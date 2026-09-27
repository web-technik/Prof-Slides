"""Diagrams package — structured diagram rendering with native Shapes."""

from prof_slide.diagrams.base import BaseDiagram
from prof_slide.diagrams.cycle import CycleDiagram
from prof_slide.diagrams.diagram_style import DiagramStyle
from prof_slide.diagrams.flowchart import FlowchartDiagram
from prof_slide.diagrams.funnel import FunnelDiagram
from prof_slide.diagrams.hierarchy import HierarchyDiagram
from prof_slide.diagrams.layout_engine import Region
from prof_slide.diagrams.matrix import MatrixDiagram
from prof_slide.diagrams.pyramid import PyramidDiagram
from prof_slide.diagrams.swot import SwotDiagram
from prof_slide.diagrams.table import TableDiagram
from prof_slide.diagrams.timeline import TimelineDiagram
from prof_slide.diagrams.venn import VennDiagram

__all__ = [
    "BaseDiagram",
    "DiagramStyle",
    "Region",
    "FlowchartDiagram",
    "TimelineDiagram",
    "SwotDiagram",
    "MatrixDiagram",
    "TableDiagram",
    "HierarchyDiagram",
    "VennDiagram",
    "CycleDiagram",
    "FunnelDiagram",
    "PyramidDiagram",
]
