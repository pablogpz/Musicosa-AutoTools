from dataclasses import dataclass
from typing import Literal


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
    artifacts_folder: str
    video_bits_folder: str
    nominations_video_options: list[NominationVideoOptions]
    overwrite: bool
    stitch_final_video: bool
    transition_options: TransitionOptions
    quiet_ffmpeg: bool
    quiet_ffmpeg_final_video: bool


@dataclass
class StageSixOutput:
    generated_video_bits_files: list[str] | None
    nominations_missing_sources: list[str] | None
    failed_video_bits: list[str] | None
    final_videos: list[str] | None
