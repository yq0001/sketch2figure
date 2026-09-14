from app.core.config import get_settings
from app.services.providers.base import AIImageProvider
from app.services.providers.claude import ClaudeImageProvider
from app.services.providers.gemini import GeminiImageProvider
from app.services.providers.openai import OpenAIImageProvider


class ProviderRegistry:
    def __init__(self) -> None:
        self._providers: dict[str, AIImageProvider] = {}
        # initialize based on current settings
        self.refresh()

    def refresh(self) -> None:
        """Reload provider instances from current settings.

        Call this after environment or settings change to ensure provider
        descriptors reflect the latest configured keys and model names.
        """
        settings = get_settings()
        self._providers = {
            "openai": OpenAIImageProvider(settings.openai_image_model, settings.openai_api_key),
            "gemini": GeminiImageProvider(settings.gemini_image_model, settings.gemini_api_key),
            "claude": ClaudeImageProvider(settings.claude_image_model, settings.anthropic_api_key),
        }

    def all(self) -> list[AIImageProvider]:
        return list(self._providers.values())

    def get(self, name: str) -> AIImageProvider:
        return self._providers[name.lower()]


provider_registry = ProviderRegistry()
