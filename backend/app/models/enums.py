from enum import StrEnum


class VersionType(StrEnum):
    ORIGINAL = "ORIGINAL"
    VANILLA = "VANILLA"
    AI_GENERATED = "AI_GENERATED"
    EDITED = "EDITED"
    FINAL = "FINAL"


class ProviderStatus(StrEnum):
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"
    UNSUPPORTED = "UNSUPPORTED"


class LabelMode(StrEnum):
    TEXT = "TEXT"
    LATEX = "LATEX"
