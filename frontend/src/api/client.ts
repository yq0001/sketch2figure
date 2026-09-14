import type { ProviderDescriptor } from '../types/provider'

async function fetchJson<T>(path: string): Promise<T> {
  const response = await fetch(path)
  if (!response.ok) {
    throw new Error(`Request failed with status ${response.status}`)
  }
  return (await response.json()) as T
}

export interface HealthResponse {
  status: string
  service: string
}

export const api = {
  health: () => fetchJson<HealthResponse>('/api/health'),
  providers: () => fetchJson<ProviderDescriptor[]>('/api/providers'),
}
