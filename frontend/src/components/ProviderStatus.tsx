import type { ProviderDescriptor } from '../types/provider'

interface ProviderStatusProps {
  provider: ProviderDescriptor
}

function humanize(name: string): string {
  if (name === 'openai') return 'OpenAI'
  if (name === 'gemini') return 'Gemini'
  if (name === 'claude') return 'Claude'
  return name
}

export function ProviderStatus({ provider }: ProviderStatusProps) {
  const canGenerate = provider.capabilities.raster_generation
  const state = canGenerate ? (provider.available ? 'Configured' : 'Not configured') : 'Unsupported'

  return (
    <article className="provider-card">
      <div>
        <h3>{humanize(provider.provider_name)}</h3>
        <p>{provider.model_name ?? 'Model not configured'}</p>
      </div>
      <span className={`status status-${state.toLowerCase().replace(' ', '-')}`}>{state}</span>
      {provider.note ? <small>{provider.note}</small> : null}
    </article>
  )
}
