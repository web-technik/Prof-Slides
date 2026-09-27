"""SVG compiler — compatibility shim.

This module now forwards to the real implementation in
``prof_slide.compiler``. New code should import from there directly::

    from prof_slide.compiler import SVGCompiler, SVGCompileError, SVGResult
"""

from __future__ import annotations

from prof_slide.compiler import SVGCompileError, SVGCompiler, SVGResult  # noqa: F401

__all__ = ["SVGCompileError", "SVGCompiler", "SVGResult"]
