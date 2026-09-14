from pathlib import Path

import pytest

from app.services.storage.filesystem import FileSystemAssetStorage


def test_storage_rejects_path_traversal(tmp_path: Path) -> None:
    storage = FileSystemAssetStorage(tmp_path)
    with pytest.raises(ValueError, match="escapes"):
        storage.resolve_asset_path("../outside.png")
