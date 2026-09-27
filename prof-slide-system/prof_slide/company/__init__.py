"""Company subpackage — template-driven PPT generation."""

from prof_slide.company.brand import BrandSpec
from prof_slide.company.content_parser import infer_component_category, load_company_content, parse_readme
from prof_slide.company.delivery_gate import CheckItem, DeliveryGate, QualityReport
from prof_slide.company.design_dna_extractor import (
    DesignDNA,
    DesignDNAExtractor,
    PagePlan,
    SlideDNA,
    TextZone,
    extract_design_context,
    extract_design_dna,
)
from prof_slide.company.image_matcher import (
    assign_images_by_size,
    auto_generate_image_prompts,
    classify_image_size,
    match_images,
)
from prof_slide.company.proposal_generator import ProposalGenerator
from prof_slide.company.prototype import clone_slide_prototype, copy_slide_shapes, prune_unreferenced_slide_parts
from prof_slide.company.scanner import ProjectAsset, ProjectScanner
from prof_slide.company.slide_extractor import SlideExtractor
from prof_slide.company.template_analyzer import TemplateAnalyzer
from prof_slide.company.version_manager import next_version, read_meta, write_meta
from prof_slide.company.vi_adapter import VITemplateAdapter
from prof_slide.company.vi_context import (
    VIBuildSession,
    design_context_from_brand_spec,
    merge_design_context,
    merge_vi_design_context,
    normalize_design_context,
    validate_variant_sequence,
)
from prof_slide.company.vi_delivery import VIBuildDelivery

__all__ = [
    "BrandSpec",
    "ProjectScanner",
    "ProjectAsset",
    "parse_readme",
    "load_company_content",
    "infer_component_category",
    "match_images",
    "assign_images_by_size",
    "auto_generate_image_prompts",
    "classify_image_size",
    "ProposalGenerator",
    "clone_slide_prototype",
    "copy_slide_shapes",
    "prune_unreferenced_slide_parts",
    "TemplateAnalyzer",
    "SlideExtractor",
    "DeliveryGate",
    "QualityReport",
    "CheckItem",
    "next_version",
    "write_meta",
    "read_meta",
    "DesignDNAExtractor",
    "DesignDNA",
    "SlideDNA",
    "TextZone",
    "PagePlan",
    "extract_design_context",
    "extract_design_dna",
    "VIBuildSession",
    "design_context_from_brand_spec",
    "merge_design_context",
    "merge_vi_design_context",
    "normalize_design_context",
    "validate_variant_sequence",
    "VITemplateAdapter",
    "VIBuildDelivery",
]
