from app.core.config import PROJECT_ROOT, Settings


def test_relative_storage_paths_resolve_from_repository_root() -> None:
    settings = Settings(_env_file=None, data_dir="./data", database_url="sqlite:///./data/test.db")
    assert settings.data_dir == (PROJECT_ROOT / "data").resolve()
    assert settings.database_url.endswith("/data/test.db")
