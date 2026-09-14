export interface ProviderCapabilities {
  raster_generation: boolean
  image_editing: boolean
  region_editing: boolean
}

export interface ProviderDescriptor {
  provider_name: string
  model_name: string | null
  available: boolean
  capabilities: ProviderCapabilities
  note: string | null
}
