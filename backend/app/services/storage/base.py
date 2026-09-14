from abc import ABC, abstractmethod
from pathlib import Path


class AssetStorage(ABC):
    @abstractmethod
    def resolve_asset_path(self, relative_path: str) -> Path:
        raise NotImplementedError
