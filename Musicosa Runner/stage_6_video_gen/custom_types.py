from dataclasses import dataclass
from typing import Literal, NamedTuple


@dataclass
class Timestamp:
    start: str
    end: str


@dataclass
class NominationVideoOptions:
    award: str
    template_friendly_name: str
    sequence_number: int
    videoclip_friendly_name: str
    timestamp: Timestamp
    width: int
    height: int
    position_top: int
    position_left: int


TransitionType = Literal[
    "custom",
    "fade",
    "wipeleft",
    "wiperight",
    "wipeup",
    "wipedown",
    "slideleft",
    "slideright",
    "slideup",
    "slidedown",
    "circlecrop",
    "rectcrop",
    "distance",
    "fadeblack",
    "fadewhite",
    "radial",
    "smoothleft",
    "smoothright",
    "smoothup",
    "smoothdown",
    "circleopen",
    "circleclose",
    "vertopen",
    "vertclose",
    "horzopen",
    "horzclose",
    "dissolve",
    "pixelize",
    "diagtl",
    "diagtr",
    "diagbl",
    "diagbr",
    "hlslice",
    "hrslice",
    "vuslice",
    "vdslice",
    "hblur",
    "fadegrays",
    "wipetl",
    "wipetr",
    "wipebl",
    "wipebr",
    "squeezeh",
    "squeezev",
    "zoomin",
    "fadefast",
    "fadeslow",
]


@dataclass
class TransitionOptions:
    presentation_duration: int
    transition_duration: int
    type: TransitionType


@dataclass
class StageSixInput:
    nominations_video_options: list[NominationVideoOptions]


class VideoGenerationResult(NamedTuple):
    generated_video_bit_files: list[str]
    skipped_video_bit_titles: list[str]
    failed_video_bit_titles: list[str]

@dataclass
class StageSixOutput:
    missing_templates: list[str]
    missing_videoclips: list[str]
    video_generation_result: VideoGenerationResult
    final_videos_files: list[str] | None
