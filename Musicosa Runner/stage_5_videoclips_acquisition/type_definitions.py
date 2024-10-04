from dataclasses import dataclass

from common.models import Entry


@dataclass
class StageFiveInput:
    artifacts_folder: str
    quiet_ffmpeg: bool
    entries: list[Entry]


@dataclass
class StageFiveOutput:
    acquired_videoclips: list[str] | None
    failed_to_acquire: list[str] | None
