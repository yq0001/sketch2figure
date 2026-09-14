import { useQuery } from '@tanstack/react-query'

import { api } from '../api/client'
import { ProviderStatus } from '../components/ProviderStatus'

export function HomePage() {
  const health = useQuery({ queryKey: ['health'], queryFn: api.health })
  const providers = useQuery({ queryKey: ['providers'], queryFn: api.providers })

  return (
    <main className="app-shell">
      <header className="topbar">
        <div>
          <span className="eyebrow">Scientific figure workspace</span>
          <h1>Sketch2Figure</h1>
        </div>
        <span className={`backend-pill ${health.data?.status === 'ok' ? 'online' : ''}`}>
          Backend {health.data?.status === 'ok' ? 'online' : 'checking'}
        </span>
      </header>

      <section className="hero-panel">
        <div>
          <p className="eyebrow">Phase 0</p>
          <h2>Architecture is ready for the first drawing workflow.</h2>
          <p>
            Projects, uploads, untouched originals, and the non-generative Vanilla pipeline arrive in
            Phase 1. AI generation controls stay disabled until their provider phases.
          </p>
        </div>
        <button type="button" disabled>
          Create project — Phase 1
        </button>
      </section>

      <section className="section-block">
        <div className="section-heading">
          <div>
            <p className="eyebrow">Provider layer</p>
            <h2>Capability status</h2>
          </div>
          {providers.isError ? <span className="error-text">Could not reach backend.</span> : null}
        </div>
        <div className="provider-grid">
          {providers.data?.map((provider) => (
            <ProviderStatus key={provider.provider_name} provider={provider} />
          ))}
        </div>
      </section>
    </main>
  )
}
