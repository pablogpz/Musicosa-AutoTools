from dataclasses import dataclass

from common.model.models import Entry


@dataclass
class StageFiveInput:
    artifacts_folder: str
    quiet_ffmpeg: bool
    entries: list[Entry]


@dataclass
class StageFiveOutput:
    acquired_videoclip_titles: list[str] | None
    failed_videoclip_titles: list[str] | None
