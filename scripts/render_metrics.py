#!/usr/bin/env python
"""Metrics-based proxy for the PNG visual review.

Why this exists: the agent driving this project cannot read image files, so the
skill's mandatory "LLM inspects the rendered PNG" gate cannot be performed by
vision. This script substitutes the *measurable* half of that gate: it renders
PPTX -> PDF -> PNG, then reports per-slide ink coverage, whitespace structure,
focal-point concentration, and PPTX-level geometry/font risks.

It CANNOT judge taste, hierarchy, or "does this look client-ready". Those stay
human/model-visual decisions. Output is evidence, not an approval.

Usage:
  python render_metrics.py <deck.pptx> [--outdir DIR] [--dpi 150]
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, asdict
from pathlib import Path


# --- render ---------------------------------------------------------------

def render(pptx: Path, outdir: Path, dpi: int) -> list[Path]:
    outdir.mkdir(parents=True, exist_ok=True)
    soffice = shutil.which("soffice") or shutil.which("soffice.bin")
    if not soffice:
        raise RuntimeError("LibreOffice (soffice) not found")
    subprocess.run(
        [soffice, "--headless", "--norestore", "--convert-to", "pdf",
         "--outdir", str(outdir), str(pptx)],
        check=True, capture_output=True, timeout=300,
    )
    pdf = outdir / (pptx.stem + ".pdf")
    if not pdf.exists():
        raise RuntimeError(f"PDF not produced: {pdf}")
    if not shutil.which("pdftoppm"):
        raise RuntimeError("Poppler (pdftoppm) not found")
    prefix = outdir / "slide"
    subprocess.run(
        ["pdftoppm", "-r", str(dpi), "-png", str(pdf), str(prefix)],
        check=True, capture_output=True, timeout=300,
    )
    return sorted(outdir.glob("slide-*.png"))


# --- image metrics --------------------------------------------------------

def _ink_mask(img, thr=0.06):
    """Boolean mask of 'has ink' (deviation from the background value).

    `thr` matters enormously for LIGHT designs: a pale panel tinted by only
    ~0.04 luminance is real, visible structure that a dark-only threshold
    (0.06) reports as empty. Callers get both a strong-ink mask and a tone
    mask so a pale blueprint sheet can be measured honestly.
    """
    import numpy as np
    arr = np.asarray(img.convert("L"), dtype="float32") / 255.0
    bg = float(np.median(arr))
    return (bg - arr) > thr, bg


def slide_metrics(png: Path, grid: int = 6) -> dict:
    from PIL import Image
    import numpy as np

    im = Image.open(png)
    W, H = im.size
    mask, bg = _ink_mask(im, 0.06)      # strong ink: text, rules, dark fills
    tone, _ = _ink_mask(im, 0.018)      # tone: includes pale tinted panels

    total = W * H
    coverage = float(mask.sum()) / total
    tone_coverage = float(tone.sum()) / total

    # zone grid -> whitespace structure
    zones = []
    for gy in range(grid):
        row = []
        for gx in range(grid):
            y0, y1 = gy * H // grid, (gy + 1) * H // grid
            x0, x1 = gx * W // grid, (gx + 1) * W // grid
            cell = mask[y0:y1, x0:x1]
            row.append(round(float(cell.mean()), 4))
        zones.append(row)

    # focus: densest cell vs median non-empty cell
    flat = [v for r in zones for v in r if v > 0.005]
    if flat:
        peak = max(flat)
        med = float(np.median(flat))
        concentration = round(peak / med, 2) if med > 0 else None
    else:
        peak, med, concentration = 0.0, 0.0, None

    # largest empty run (dead whitespace) - scan rows/cols with no ink
    row_ink = mask.mean(axis=1)
    col_ink = mask.mean(axis=0)

    def largest_run(arr, thr=0.001):
        best = cur = 0
        for v in arr:
            cur = 0 if v <= thr else cur + 1
            best = max(best, cur)
        return int(best)

    dead_h = largest_run(row_ink)
    dead_v = largest_run(col_ink)

    # edge safety: ink touching the outer 1.5% -> possible bleed/clipping
    m = int(min(W, H) * 0.015)
    edge_ink = float(
        mask[:m, :].mean() + mask[-m:, :].mean()
        + mask[:, :m].mean() + mask[:, -m:].mean()
    ) / 4.0

    return {
        "png": str(png),
        "size": [W, H],
        "bg_luma": round(bg, 3),
        "ink_coverage": round(coverage, 4),
        "tone_coverage": round(tone_coverage, 4),
        "empty_zone_frac": round(
            sum(1 for r in zones for v in r if v <= 0.005) / (grid * grid), 3
        ),
        "peak_zone_ink": round(peak, 4),
        "median_active_zone_ink": round(med, 4),
        "focus_concentration": concentration,
        "dead_band_px_h": dead_h,
        "dead_band_frac_h": round(dead_h / H, 3),
        "dead_band_frac_v": round(dead_v / W, 3),
        "edge_ink_frac": round(edge_ink, 5),
        "zones": zones,
    }


# --- pptx geometry / typography -------------------------------------------

@dataclass
class ShapeRisk:
    slide: int
    shape_id: int
    name: str
    kind: str
    risk: str
    detail: str


# Small text is only a defect if it is BODY text. Footers, page numbers,
# source lines, captions and kickers are legitimately at the caption/metadata
# floor (9pt in most readability contracts), so a flat threshold produces noise.
METADATA_ROLE = re.compile(
    r"footer|caption|kicker|page-number|readout|source|note|credit|eyebrow"
    r"|annotation|title-block|label|partnum|dim",
    re.I,
)


def pptx_risks(pptx: Path, min_body_pt: float = 12.0,
               min_meta_pt: float = 9.0) -> list[ShapeRisk]:
    from pptx import Presentation
    from pptx.util import Emu

    prs = Presentation(str(pptx))
    SW, SH = prs.slide_width, prs.slide_height
    out: list[ShapeRisk] = []

    for idx, slide in enumerate(prs.slides, start=1):
        for sh in slide.shapes:
            risks: list[tuple[str, str]] = []

            # off-canvas / out of bounds
            try:
                if sh.left is None or sh.top is None:
                    continue
                if sh.left < -Emu(0) or sh.top < 0 or \
                   sh.left + (sh.width or 0) > SW + Emu(1) or \
                   sh.top + (sh.height or 0) > SH + Emu(1):
                    risks.append((
                        "out_of_bounds",
                        f"box=({sh.left},{sh.top},{sh.width},{sh.height}) "
                        f"canvas=({SW},{SH})",
                    ))
            except Exception:
                pass

            # tiny text, judged against the role's own floor
            if sh.has_text_frame:
                is_meta = bool(METADATA_ROLE.search(sh.name or ""))
                floor = min_meta_pt if is_meta else min_body_pt
                for para in sh.text_frame.paragraphs:
                    for run in para.runs:
                        if run.font.size is not None:
                            pt = run.font.size.pt
                            txt = (run.text or "").strip()
                            if txt and pt < floor:
                                risks.append((
                                    "meta_font_too_small" if is_meta
                                    else "body_font_too_small",
                                    f"{pt}pt < {floor}pt floor on {txt[:48]!r}",
                                ))

            for risk, detail in risks:
                out.append(ShapeRisk(idx, sh.shape_id, sh.name,
                                     str(sh.shape_type), risk, detail))
    return out


# --- main -----------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("pptx", type=Path)
    ap.add_argument("--outdir", type=Path, default=None)
    ap.add_argument("--dpi", type=int, default=150)
    ap.add_argument("--min-body-pt", type=float, default=12.0)
    ap.add_argument("--min-meta-pt", type=float, default=9.0)
    ap.add_argument("--json-out", type=Path, default=None)
    a = ap.parse_args()

    tmp = None
    if a.outdir is None:
        tmp = Path(tempfile.mkdtemp(prefix="render-metrics-"))
        outdir = tmp
    else:
        outdir = a.outdir

    try:
        pngs = render(a.pptx, outdir, a.dpi)
        metrics = [slide_metrics(p) for p in pngs]
        risks = [asdict(r) for r in pptx_risks(a.pptx, a.min_body_pt, a.min_meta_pt)]

        report = {
            "pptx": str(a.pptx),
            "dpi": a.dpi,
            "slide_count": len(pngs),
            "note": (
                "Metrics only. Ink/whitespace/focus structure is objective; "
                "taste, hierarchy and 'client-ready' judgment are NOT covered "
                "here and still require a human or a vision-capable reviewer."
            ),
            "slides": metrics,
            "pptx_risks": risks,
            "risk_counts": {
                k: sum(1 for r in risks if r["risk"] == k)
                for k in sorted({r["risk"] for r in risks})
            },
        }

        if a.json_out:
            a.json_out.parent.mkdir(parents=True, exist_ok=True)
            a.json_out.write_text(json.dumps(report, indent=2))

        # console summary
        print(f"{a.pptx}  ->  {len(pngs)} slides @ {a.dpi}dpi")
        print(f"{'#':>2}  {'ink':>6} {'tone':>6} {'empty':>6} {'focus':>6} "
              f"{'deadH':>6} {'edge':>7}")
        for i, m in enumerate(metrics, start=1):
            print(f"{i:>2}  {m['ink_coverage']:>6.3f} "
                  f"{m['tone_coverage']:>6.3f} "
                  f"{m['empty_zone_frac']:>6.3f} "
                  f"{str(m['focus_concentration']):>6} "
                  f"{m['dead_band_frac_h']:>6.3f} "
                  f"{m['edge_ink_frac']:>7.5f}")
        print(f"\npptx risks: {report['risk_counts'] or 'none'}")
        for r in risks[:20]:
            print(f"  slide {r['slide']} {r['name']} [{r['risk']}] {r['detail']}")
        if a.json_out:
            print(f"\njson: {a.json_out}")
        return 0
    finally:
        if tmp and not a.outdir:
            print(f"(renders kept at {tmp})")


if __name__ == "__main__":
    sys.exit(main())
