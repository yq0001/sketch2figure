from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.core.config import get_settings
from app.core.logging import configure_logging
from app.services.providers import registry as provider_registry_module

settings = get_settings()
configure_logging(settings.log_level)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    settings.data_dir.mkdir(parents=True, exist_ok=True)
    # Ensure provider registry reads the latest settings (useful when .env changes)
    try:
        provider_registry_module.provider_registry.refresh()
    except Exception:
        # don't fail startup if refresh isn't possible; providers will be lazy
        pass
    yield


app = FastAPI(title=settings.app_name, version="0.1.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1)(:\\d+)?$",
    allow_credentials=False,
    allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)
app.include_router(router)


# Simple dev-friendly CORS fallback: ensure requests from localhost variants get Access-Control-Allow-Origin
@app.middleware("http")
async def dev_cors_middleware(request, call_next):
    response = await call_next(request)
    origin = request.headers.get("origin")
    if origin and ("localhost" in origin or "127.0.0.1" in origin):
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Methods"] = "GET,POST,PUT,PATCH,DELETE,OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "*"
    return response
