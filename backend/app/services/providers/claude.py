from typing import Any

from app.schemas.provider import ProviderCapabilities, ProviderDescriptor
from app.services.providers.base import AIImageProvider, ProviderImageResult


class ClaudeImageProvider(AIImageProvider):
    provider_name = "claude"

    def capabilities(self) -> ProviderCapabilities:
        # Phase 4 will verify current Anthropic raster-image capabilities against official docs.
        # Keep unsupported behavior explicit until then; never substitute another provider.
        return ProviderCapabilities(
            raster_generation=False, image_editing=False, region_editing=False
        )

    def descriptor(self) -> ProviderDescriptor:
        descriptor = super().descriptor()
        descriptor.available = False
        descriptor.note = "Raster image generation capability will be verified in Phase 4."
        return descriptor

    async def generate_from_sketch(self, *args: Any, **kwargs: Any) -> ProviderImageResult:
        raise NotImplementedError("Claude raster image generation is not enabled in Phase 0.")

    async def edit_image(self, *args: Any, **kwargs: Any) -> ProviderImageResult:
        raise NotImplementedError("Claude raster image editing is not enabled in Phase 0.")
