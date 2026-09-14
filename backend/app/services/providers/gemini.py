from typing import Any

from app.schemas.provider import ProviderCapabilities
from app.services.providers.base import AIImageProvider, ProviderImageResult


class GeminiImageProvider(AIImageProvider):
    provider_name = "gemini"

    def capabilities(self) -> ProviderCapabilities:
        return ProviderCapabilities(
            raster_generation=True, image_editing=True, region_editing=False
        )

    async def generate_from_sketch(self, *args: Any, **kwargs: Any) -> ProviderImageResult:
        raise NotImplementedError("Gemini image generation is implemented in Phase 3.")

    async def edit_image(self, *args: Any, **kwargs: Any) -> ProviderImageResult:
        raise NotImplementedError("Gemini image editing is implemented in a later phase.")
