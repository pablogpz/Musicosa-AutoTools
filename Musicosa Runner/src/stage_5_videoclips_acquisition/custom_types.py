from dataclasses import dataclass
from typing import NamedTuple

from common.model.models import Videoclip


@dataclass
class StageFiveInput:
    videoclips: list[Videoclip]


class VideoclipsDownloadResult(NamedTuple):
    downloaded_videoclip_titles: list[str]
    skipped_videoclip_titles: list[str]
    failed_videoclip_titles: list[str]


@dataclass
class StageFiveOutput:
    download_result: VideoclipsDownloadResult
