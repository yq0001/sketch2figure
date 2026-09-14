from pathlib import Path

from app.services.storage.base import AssetStorage


class FileSystemAssetStorage(AssetStorage):
    def __init__(self, root: Path) -> None:
        self.root = root.resolve()

    def resolve_asset_path(self, relative_path: str) -> Path:
        candidate = (self.root / relative_path).resolve()
        if candidate != self.root and self.root not in candidate.parents:
            raise ValueError("Asset path escapes the configured storage root.")
        return candidate
