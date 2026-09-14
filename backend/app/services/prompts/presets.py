from enum import StrEnum


class StylePreset(StrEnum):
    SCIENTIFIC_PUBLICATION_COLOR = "scientific_publication_color"
    JOURNAL_LINE_ART_BW = "journal_line_art_bw"
    SCIENTIFIC_PRESENTATION = "scientific_presentation"
    BIOLOGICAL_ILLUSTRATION = "biological_illustration"
    CUSTOM = "custom"


STYLE_GUIDANCE: dict[StylePreset, str] = {
    StylePreset.SCIENTIFIC_PUBLICATION_COLOR: (
        "Clean scientific journal aesthetic with a white background, restrained professional "
        "colors, "
        "crisp shapes, strong visual hierarchy, and subtle depth only when useful."
    ),
    StylePreset.JOURNAL_LINE_ART_BW: (
        "Black-and-white journal line art with clean outlines, consistent stroke weights, and "
        "little or no shading."
    ),
    StylePreset.SCIENTIFIC_PRESENTATION: (
        "Presentation-quality scientific graphic with attractive restrained colors, stronger "
        "contrast, and clear hierarchy."
    ),
    StylePreset.BIOLOGICAL_ILLUSTRATION: (
        "Polished biological illustration with intentional natural forms, professional rendering, "
        "and diagram-friendly clarity."
    ),
    StylePreset.CUSTOM: "",
}

SCIENTIFIC_FIDELITY_RULE = (
    "Use the source sketch as the scientific and compositional reference. Improve visual quality, "
    "alignment, proportions, "
    "perspective, spacing, biological forms, line quality, symbols, and color palette. Preserve "
    "the scientific meaning, "
    "major structures, arrows, and relationships. Do not invent biological mechanisms, pathways, "
    "labels, experimental "
    "conclusions, or scientifically meaningful structures not supported by the source. Avoid "
    "unnecessary rasterized text "
    "because final labels are applied as editable overlays."
)
