from dataclasses import dataclass


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


@dataclass
class StageSixInput:
    artifacts_folder: str
    video_bits_folder: str
    nominations_video_options: list[NominationVideoOptions]
    overwrite: bool
    quiet_ffmpeg: bool


@dataclass
class StageSixOutput:
    generated_video_bits_files: list[str] | None
    nominations_missing_sources: list[str] | None
    failed_video_bits: list[str] | None
