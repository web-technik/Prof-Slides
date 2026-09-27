# presentation-skill

A skill for coding agents that produces editable PowerPoint decks from structured source files. The idea is to treat a deck like code: `outline.json` is the source, scripts build the `.pptx`, and a validation loop checks layout, density, and design-taste issues before delivery.

*One topic, eight styles. The title and process slides change structure while the evidence stays fixed. The PowerPoints remain editable.*

Ask an agent for a lab report, board memo, investor update, clinical dashboard, policy brief, or scientific figure deck. The skill writes source JSON, routes style and content structure, builds an editable `.pptx`, and runs QA instead of shipping a screenshot or a stack of centered bullets.

## Why

Most agent-built slide decks pass automated checks and still look bad. Dead whitespace, centered body text, the same three-card layout used five times in a row, generic stock-icon clusters. They feel like AI output even when the words are right.

This skill encodes deck design as constraints instead of vibes. A variant grammar restricts what a slide can be. A preset system fixes palette, typography, and density per style family. A descriptor-only corpus of public deck-like records gives the agent style context to pick from instead of inventing from scratch. A QA loop catches layout regressions before the deck ships.

## When to use this skill

Reach for it when an agent needs to:

- build a one-off PowerPoint `.pptx`, slide deck, or presentation from a single prompt (quick-deck mode, no workspace needed)
- generate a `.pptx` from a structured `outline.json`
- redesign, rebuild, or extend an existing slide deck
- run layout and design QA on a generated deck
- assemble a lab, clinical, board, investor, or editorial deck with consistent style
- maintain a reusable presentation workspace that can be re-rendered later

Quick-deck mode is the right path for one-shot 5-10 slide decks. Workspace mode is for decks that will be iterated, audited, or rebuilt later.

Skip it for text-only brainstorming where no deck artifact is needed, or for direct edits to a generated `.pptx` when its workspace source files are available (fix the source instead).

Skill name: `presentation-skill`. Aliases for fuzzy skill matching and search: `powerpoint-deck-builder`, `pptx-skill`, PowerPoint skill, PPTX skill, slide-deck generator, slides generator, deck builder, presentation generator, presentation maker, PowerPoint generator, agent presentation skill, Codex presentation skill, ChatGPT presentation skill.

## What's actually in the box

- **A pptxgenjs renderer with 16 content variants plus title and section slides.** `standard`, `split`, `cards-2`, `cards-3`, `timeline`, `stats`, `kpi-hero`, `comparison-2col`, `matrix`, `chart`, `table`, `lab-run-results`, `image-sidebar`, `scientific-figure`, `flow` (Mermaid), and `generated-image`. Each variant has its own layout discipline so a deck doesn't collapse into bullet-list-after-bullet-list.
- **A preset system across 13 style families.** Lab report, executive clinical, board risk memo, investor reveal, editorial report, civic science policy, and so on. Each owns a palette, font pair, density profile, and bounded visual interpretation.
- **Eight full-deck composition grammars above the presets.** Answer Pyramid, Evidence Plate, Care Pathway, Editorial Spread, Thesis Stage, Operating Grid, Public Docket, and Telemetry Canvas own role contracts for title, section, evidence, comparison, chart, table, decision, and references. A semantic render plan keeps role and visual variant separate, uses v2 geometry only for supported pairs, and records explicit v1/legacy fallbacks instead of silently substituting layouts. Slide overrides stay bounded to `primary`, `alternate`, or `dense`.
- **A descriptor-only style corpus (~2,200 records) atomized into a composable token atlas.** The corpus carries described palettes, layouts, density patterns, and structural motifs from public deck-like sources (no copied assets). It's processed into 311 atoms across 12 types. New workspaces route the topic to a preset and independently select a composition grammar, so an advanced model can mix bounded design signals instead of receiving one static template.
- **A lightweight model-adaptive entrypoint.** `present.py` offers compact briefs, optional intake questions, and content-matched style previews. Luna, Terra, Sol, Astra, or a future model can use the same source contracts; no multi-agent setup is required. Focused repair packets and opt-in render caching keep iteration small without skipping QA.
- **A layered QA loop with exact-review receipts.** Geometry, rendered-image inspection, placeholder detection, design rules, and optional accessibility checks catch deterministic failures. For high-stakes delivery, a human/model verdict can be bound to the exact PPTX and rendered-slide hashes, so a rebuilt deck cannot reuse stale approval.
- **Workspace mode with a versioned Deck IR.** Planning sources live beside `outline.json`; each build derives a deterministic coordinate-free `deck_ir.json` with stable object IDs, semantic intent, evidence links, and editability metadata. Readiness diagnostics tell the agent what to fix next instead of re-running blind.
- **Preserve-by-default reference editing.** A standalone `.pptx` can be inspected into stable slide/shape IDs, patched through registered text/alt-text actions with preconditions, and checked to prove untouched geometry, style, and text stayed unchanged.
- **An honest cross-generator benchmark protocol.** A frozen hidden prompt matrix, exact artifact ingestion, hard gates, blinded Content/Aesthetics/Editability review, and paired bootstrap analysis support same-denominator Codex-native, Claude Code, and skill comparisons. The harness never pretends it executed an external generator.

## What people actually build with this

A few concrete use cases this skill is set up for, drawn from the variants and presets it ships with:

- **Lab and clinical data reports.** CSV in, scientific-figure slides with subfigure labels out. `lab-run-results` slides use semantic table coloring (red/green/yellow for pass/fail/status). `image-sidebar` for microscopy panels and workflow diagrams.
- **Investor and board decks.** `kpi-hero`, `stats`, and `comparison-2col` variants with the `bold-startup-narrative` or `data-heavy-boardroom` presets. Generated charts cropped, slide-sized, and readable before assembly.
- **Editorial and policy briefs.** `editorial-minimal`, `paper-journal`, and `warm-terracotta` presets with `image-sidebar`, `matrix`, `timeline`, and concise synthesis variants. Built for proof-burden + audience-posture decks rather than 10-bullet recap slides.
- **Design gallery testing.** Build the same outline across all 13 presets with multiple header variants to see how a content shape lands in different design families. Useful when you don't know which preset fits a topic.

- **Topics:** powerpoint, pptx, presentation, slide-deck, slides, deck-generator, presentation-generator, agent-skill, codex-skill, chatgpt-skill, openai-agents, pptxgenjs, python-pptx, deck-design, slide-qa, layout-validation, presentation-workspace, lab-report-deck, investor-deck, board-deck, scientific-figure-slides
