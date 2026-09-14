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
        If `get_settings()` does not show values (possible with caching),
        attempt to read them directly from a `.env` file in the project root
        as a fallback.
        """
        settings = get_settings()

        # fallback parser for .env if settings don't contain values
        def read_env_file() -> dict[str, str]:
            try:
                from app.core.config import PROJECT_ROOT
                env_path = PROJECT_ROOT / ".env"
                if not env_path.exists():
                    return {}
                data: dict[str, str] = {}
                for line in env_path.read_text(encoding="utf-8").splitlines():
                    line = line.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    k, v = line.split("=", 1)
                    data[k.strip()] = v.strip()
                return data
            except Exception:
                return {}

        envvals = read_env_file()

        def pick(setting_val: str | None, envkey: str) -> str | None:
            if setting_val:
                return setting_val
            return envvals.get(envkey) or None

        openai_model = pick(settings.openai_image_model, "OPENAI_IMAGE_MODEL")
        openai_key = pick(settings.openai_api_key, "OPENAI_API_KEY")
        gemini_model = pick(settings.gemini_image_model, "GEMINI_IMAGE_MODEL")
        gemini_key = pick(settings.gemini_api_key, "GEMINI_API_KEY")
        claude_model = pick(settings.claude_image_model, "CLAUDE_IMAGE_MODEL")
        claude_key = pick(settings.anthropic_api_key, "ANTHROPIC_API_KEY")

        self._providers = {
            "openai": OpenAIImageProvider(openai_model, openai_key),
            "gemini": GeminiImageProvider(gemini_model, gemini_key),
            "claude": ClaudeImageProvider(claude_model, claude_key),
        }

    def all(self) -> list[AIImageProvider]:
        return list(self._providers.values())

    def get(self, name: str) -> AIImageProvider:
        return self._providers[name.lower()]


provider_registry = ProviderRegistry()
