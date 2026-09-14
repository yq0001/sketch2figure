from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from app.models.enums import ProviderStatus
from app.schemas.provider import ProviderCapabilities, ProviderDescriptor


@dataclass(slots=True)
class ProviderImageResult:
    provider: str
    model: str | None
    status: ProviderStatus
    source_version_id: str
    generated_asset_path: Path | None
    original_user_instruction: str
    final_provider_prompt: str
    width: int | None = None
    height: int | None = None
    latency_ms: int | None = None
    error: str | None = None
    generation_parameters: dict[str, Any] | None = None
    usage_metadata: dict[str, Any] | None = None


class AIImageProvider(ABC):
    provider_name: str

    def __init__(self, model_name: str | None, api_key: str | None) -> None:
        self.model_name = model_name or None
        self._api_key = api_key or None

    def is_available(self) -> bool:
        return bool(self._api_key and self.model_name)

    @abstractmethod
    def capabilities(self) -> ProviderCapabilities:
        raise NotImplementedError

    def descriptor(self) -> ProviderDescriptor:
        return ProviderDescriptor(
            provider_name=self.provider_name,
            model_name=self.model_name,
            available=self.is_available(),
            capabilities=self.capabilities(),
        )

    @abstractmethod
    async def generate_from_sketch(self, *args: Any, **kwargs: Any) -> ProviderImageResult:
        raise NotImplementedError

    @abstractmethod
    async def edit_image(self, *args: Any, **kwargs: Any) -> ProviderImageResult:
        raise NotImplementedError

    async def health_check(self) -> bool:
        return self.is_available()
