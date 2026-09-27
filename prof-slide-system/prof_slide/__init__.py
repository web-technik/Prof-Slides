"""
prof-slide: Python library for LLMs to generate PowerPoint presentations.

Quick start:
    from prof_slide import generate_ppt
    result = generate_ppt("AI startup pitch deck", style="dark cyberpunk")

Build mode (pixel-perfect control):
    from prof_slide.tools.shapes import rect
    from prof_slide.tools.text import text
    from prof_slide.tools.cards import kpi_card, page_header
    from prof_slide.core.pipeline import Presentation

Available data (40,000+ style combinations):
    from prof_slide.data import PALETTES    # 192 color schemes
    from prof_slide.data import TYPOGRAPHY  # 74 font pairs
    from prof_slide.data import STYLES      # 84 style presets

Shape functions:
    rect, rounded_rect, oval, hexagon, diamond, star, triangle, arrow, chevron

Text functions:
    text, multiline, gradient_text, dramatic_text, vertical_text

Chart functions:
    bar_chart, donut_chart, native_chart, comparison_bars

Component functions:
    kpi_card, highlight_cards, code_block, section_divider, hero_slide

Image functions:
    cover_image, circle_image, ai_image

Layout functions:
    page_header, top_bar, page_number

Effect functions:
    text_shadow, text_glow, shape_3d, pattern_fill
"""

from __future__ import annotations

__version__ = "0.1.0"

from prof_slide.ai import fetch_image
from prof_slide.core.pipeline import Presentation, generate_ppt
from prof_slide.data import PALETTES, STYLES, TYPOGRAPHY
from prof_slide.company.design_dna_extractor import extract_design_context, extract_design_dna
from prof_slide.company.vi_context import (
    VIBuildSession,
    design_context_from_brand_spec,
    merge_design_context,
    merge_vi_design_context,
    normalize_design_context,
)
from prof_slide.renderer.theme import recommend_styles, validate_resolved_theme
from prof_slide.renderer.theme_context import set_presentation_theme, set_slide_theme
from prof_slide.tools.svg import svg_chart

__all__ = [
    "__version__",
    "PALETTES",
    "TYPOGRAPHY",
    "STYLES",
    "Presentation",
    "generate_ppt",
    "fetch_image",
    "extract_design_dna",
    "extract_design_context",
    "VIBuildSession",
    "design_context_from_brand_spec",
    "merge_design_context",
    "merge_vi_design_context",
    "normalize_design_context",
    "recommend_styles",
    "validate_resolved_theme",
    "set_presentation_theme",
    "set_slide_theme",
    "svg_chart",
]
