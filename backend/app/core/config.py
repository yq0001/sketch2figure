from functools import lru_cache
from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[3]
ENV_FILE = PROJECT_ROOT / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "Sketch2Figure"
    app_env: str = "development"
    app_host: str = "127.0.0.1"
    app_port: int = 8000
    frontend_origin: str = "http://localhost:5173"
    log_level: str = "INFO"

    database_url: str = "sqlite:///./data/sketch2figure.db"
    data_dir: Path = Path("./data")
    max_upload_mb: int = Field(default=25, ge=1, le=500)

    openai_api_key: str | None = None
    gemini_api_key: str | None = None
    anthropic_api_key: str | None = None

    openai_image_model: str | None = None
    gemini_image_model: str | None = None
    claude_image_model: str | None = None

    run_external_ai_tests: bool = False

    @field_validator("data_dir", mode="after")
    @classmethod
    def resolve_data_dir(cls, value: Path) -> Path:
        return value if value.is_absolute() else (PROJECT_ROOT / value).resolve()

    @field_validator("database_url", mode="after")
    @classmethod
    def resolve_sqlite_database_url(cls, value: str) -> str:
        prefix = "sqlite:///"
        if not value.startswith(prefix):
            return value
        raw_path = value[len(prefix) :]
        path = Path(raw_path)
        if path.is_absolute():
            return value
        absolute = (PROJECT_ROOT / path).resolve().as_posix()
        return f"sqlite:///{absolute}"

    @property
    def cors_origins(self) -> list[str]:
        return [self.frontend_origin]


@lru_cache
def get_settings() -> Settings:
    return Settings()
