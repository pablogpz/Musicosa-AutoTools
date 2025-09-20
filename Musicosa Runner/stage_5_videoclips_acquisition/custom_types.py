from dataclasses import dataclass

from common.model.models import Videoclip


@dataclass
class StageFiveInput:
    videoclips: list[Videoclip]


@dataclass
class StageFiveOutput:
    acquired_videoclip_titles: list[str] | None
    failed_videoclip_titles: list[str] | None
