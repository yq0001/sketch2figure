from fastapi import APIRouter

from app.schemas.provider import ProviderDescriptor
from app.services.providers import provider_registry

router = APIRouter(prefix="/api")


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "sketch2figure-backend"}


@router.get("/providers", response_model=list[ProviderDescriptor])
def providers() -> list[ProviderDescriptor]:
    return [provider.descriptor() for provider in provider_registry.all()]


@router.get("/providers/capabilities", response_model=list[ProviderDescriptor])
def provider_capabilities() -> list[ProviderDescriptor]:
    return providers()
