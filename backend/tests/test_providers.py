from app.services.providers.registry import ProviderRegistry


def test_provider_registry_exposes_all_first_class_providers() -> None:
    descriptors = {
        provider.provider_name: provider.descriptor() for provider in ProviderRegistry().all()
    }
    assert set(descriptors) == {"openai", "gemini", "claude"}
    assert descriptors["openai"].capabilities.raster_generation is True
    assert descriptors["gemini"].capabilities.raster_generation is True
    assert descriptors["claude"].capabilities.raster_generation is False
