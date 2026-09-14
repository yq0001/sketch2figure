from app.services.prompts.builder import build_base_prompt
from app.services.prompts.presets import StylePreset


def test_prompt_builder_preserves_instruction_and_scientific_fidelity_rule() -> None:
    instruction = "Make the cell diagram publication quality."
    prompt = build_base_prompt(instruction, StylePreset.SCIENTIFIC_PUBLICATION_COLOR)
    assert instruction in prompt
    assert "Preserve the scientific meaning" in prompt
    assert "Avoid unnecessary rasterized text" in prompt
