from dataclasses import dataclass
from typing import Literal


@dataclass
class Timestamp:
    start: str
    end: str


@dataclass
class EntryVideoOptions:
    entry_id: str
    entry_title: str
    sequence_number: int
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
    entries_video_options: list[EntryVideoOptions]
    overwrite: bool
    stitch_final_video: bool
    final_video_name: str
    transition_options: TransitionOptions
    quiet_ffmpeg: bool
    quiet_ffmpeg_final_video: bool


@dataclass
class StageSixOutput:
    generated_video_bits_files: list[str] | None
    entries_missing_sources: list[str] | None
    failed_video_bits: list[str] | None
    final_video: str | None
