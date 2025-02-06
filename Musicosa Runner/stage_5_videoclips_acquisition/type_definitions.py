from dataclasses import dataclass

from common.model.models import Videoclip


@dataclass
class StageFiveInput:
    artifacts_folder: str
    quiet_ffmpeg: bool
    videoclips: list[Videoclip]


@dataclass
class StageFiveOutput:
    acquired_videoclips: list[str] | None
    failed_to_acquire: list[str] | None
