from app.services.prompts.presets import SCIENTIFIC_FIDELITY_RULE, STYLE_GUIDANCE, StylePreset


def build_base_prompt(user_instruction: str, style: StylePreset) -> str:
    parts = [user_instruction.strip()]
    if STYLE_GUIDANCE[style]:
        parts.append(STYLE_GUIDANCE[style])
    parts.append(SCIENTIFIC_FIDELITY_RULE)
    return "\n\n".join(part for part in parts if part)
