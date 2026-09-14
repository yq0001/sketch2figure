from pydantic import BaseModel


class ProviderCapabilities(BaseModel):
    raster_generation: bool
    image_editing: bool
    region_editing: bool


class ProviderDescriptor(BaseModel):
    provider_name: str
    model_name: str | None
    available: bool
    capabilities: ProviderCapabilities
    note: str | None = None
