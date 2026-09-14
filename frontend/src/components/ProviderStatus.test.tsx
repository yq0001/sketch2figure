import '@testing-library/jest-dom/vitest'
import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'

import { ProviderStatus } from './ProviderStatus'

describe('ProviderStatus', () => {
  it('shows unsupported for a provider without raster generation', () => {
    render(
      <ProviderStatus
        provider={{
          provider_name: 'claude',
          model_name: null,
          available: false,
          capabilities: { raster_generation: false, image_editing: false, region_editing: false },
          note: 'Raster generation unavailable.',
        }}
      />,
    )

    expect(screen.getByText('Claude')).toBeInTheDocument()
    expect(screen.getByText('Unsupported')).toBeInTheDocument()
  })
})
