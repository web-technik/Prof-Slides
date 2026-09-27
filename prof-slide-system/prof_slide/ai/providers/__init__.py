"""AI providers — image generation adapters."""

from prof_slide.ai.providers.dalle import DallEProvider
from prof_slide.ai.providers.gemini import GeminiProvider
from prof_slide.ai.providers.gpt_image import GPTImageProvider
from prof_slide.ai.providers.kimi import KimiProvider
from prof_slide.ai.providers.seedream import SeedreamProvider
from prof_slide.ai.providers.wanx import WanxProvider

__all__ = [
    "SeedreamProvider",
    "GPTImageProvider",
    "DallEProvider",
    "GeminiProvider",
    "WanxProvider",
    "KimiProvider",
]
