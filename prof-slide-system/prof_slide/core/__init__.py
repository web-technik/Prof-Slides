"""Core planning, rendering, and BuildSpec contracts."""

from prof_slide.core.content import ContentGenerator, PageContent
from prof_slide.core.decider import DesignDecider, PageDesign
from prof_slide.core.pipeline import Presentation
from prof_slide.core.planner import PagePlan, StoryPlan, StoryPlanner

from .build_spec import render_build_spec

__all__ = [
    "Presentation",
    "StoryPlanner",
    "StoryPlan",
    "PagePlan",
    "DesignDecider",
    "PageDesign",
    "ContentGenerator",
    "PageContent",
    "render_build_spec",
]
