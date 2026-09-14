from typing import Any

from app.schemas.provider import ProviderCapabilities
from app.services.providers.base import AIImageProvider, ProviderImageResult


class OpenAIImageProvider(AIImageProvider):
    provider_name = "openai"

    def capabilities(self) -> ProviderCapabilities:
        return ProviderCapabilities(raster_generation=True, image_editing=True, region_editing=True)

    async def generate_from_sketch(self, *args: Any, **kwargs: Any) -> ProviderImageResult:
        raise NotImplementedError("OpenAI image generation is implemented in Phase 2.")

    async def edit_image(self, *args: Any, **kwargs: Any) -> ProviderImageResult:
        raise NotImplementedError("OpenAI image editing is implemented in a later phase.")
