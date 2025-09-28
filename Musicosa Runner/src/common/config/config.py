from dataclasses import dataclass

from common.config.defaults import DEFAULT_ARTIFACTS_FOLDER, DEFAULT_START_FROM_STAGE, DEFAULT_STITCH_FINAL_VIDEO_FLAG, \
    DEFAULT_FORMS_FOLDER, DEFAULT_VALID_TITLES_FILE, DEFAULT_TEMPLATES_API_URL, DEFAULT_PRESENTATIONS_API_URL, \
    DEFAULT_GENERATION_RETRY_ATTEMPTS, DEFAULT_OVERWRITE_TEMPLATES, DEFAULT_OVERWRITE_PRESENTATIONS, \
    DEFAULT_STAGE_5_QUIET_FFMPEG, DEFAULT_VIDEO_BITS_FOLDER, DEFAULT_OVERWRITE_VIDEO_BITS, DEFAULT_FINAL_VIDEO_NAME, \
    DEFAULT_PRESENTATION_DURATION, DEFAULT_TRANSITION_DURATION, DEFAULT_TRANSITION_TYPE, DEFAULT_STAGE_6_QUIET_FFMPEG, \
    DEFAULT_QUIET_FFMPEG_FINAL_VIDEO, DEFAULT_CONTESTANT_NAME_COORDS, DEFAULT_ENTRIES_DATA_COORDS, DEFAULT_USE_COOKIES
from common.custom_types import Stage


# NOTE: Keep dataclasses in sync with TOML keys

@dataclass
class StageOneConfig:
    forms_folder: str
    valid_titles_file: str
    contestant_name_coords: str
    entries_data_coords: str

    def __init__(self, forms_folder: str = DEFAULT_FORMS_FOLDER,
                 valid_titles_file: str = DEFAULT_VALID_TITLES_FILE,
                 contestant_name_coords: str = DEFAULT_CONTESTANT_NAME_COORDS,
                 entries_data_coords: str = DEFAULT_ENTRIES_DATA_COORDS):
        forms_folder = forms_folder.strip()

        self.forms_folder = forms_folder.removesuffix("/") if forms_folder.endswith("/") else forms_folder
        self.valid_titles_file = valid_titles_file.strip()
        self.contestant_name_coords = contestant_name_coords.strip()
        self.entries_data_coords = entries_data_coords.strip()


@dataclass
class StageFourConfig:
    templates_api_url: str
    presentations_api_url: str
    gen_retry_attempts: int
    overwrite_templates: bool
    overwrite_presentations: bool

    def __init__(self, templates_api_url: str = DEFAULT_TEMPLATES_API_URL,
                 presentations_api_url: str = DEFAULT_PRESENTATIONS_API_URL,
                 gen_retry_attempts: int = DEFAULT_GENERATION_RETRY_ATTEMPTS,
                 overwrite_templates: bool = DEFAULT_OVERWRITE_TEMPLATES,
                 overwrite_presentations: bool = DEFAULT_OVERWRITE_PRESENTATIONS):
        templates_api_url = templates_api_url.strip()

        self.templates_api_url = templates_api_url.removesuffix("/") if templates_api_url.endswith("/") \
            else templates_api_url

        presentations_api_url = presentations_api_url.strip()

        self.presentations_api_url = presentations_api_url.removesuffix("/") if presentations_api_url.endswith("/") \
            else presentations_api_url

        self.gen_retry_attempts = gen_retry_attempts
        self.overwrite_templates = overwrite_templates
        self.overwrite_presentations = overwrite_presentations


@dataclass
class StageFiveConfig:
    use_cookies: bool
    quiet_ffmpeg: bool

    def __init__(self, use_cookies: bool = DEFAULT_USE_COOKIES, quiet_ffmpeg: bool = DEFAULT_STAGE_5_QUIET_FFMPEG):
        self.use_cookies = use_cookies
        self.quiet_ffmpeg = quiet_ffmpeg


@dataclass
class StageSixConfig:
    video_bits_folder: str
    overwrite_video_bits: bool
    final_video_name: str
    presentation_duration: int
    transition_duration: int
    transition_type: str
    quiet_ffmpeg: bool
    quiet_ffmpeg_final_video: bool

    def __init__(self, video_bits_folder: str = DEFAULT_VIDEO_BITS_FOLDER,
                 overwrite_video_bits: bool = DEFAULT_OVERWRITE_VIDEO_BITS,
                 final_video_name: str = DEFAULT_FINAL_VIDEO_NAME,
                 presentation_duration: int = DEFAULT_PRESENTATION_DURATION,
                 transition_duration: int = DEFAULT_TRANSITION_DURATION,
                 transition_type: str = DEFAULT_TRANSITION_TYPE,
                 quiet_ffmpeg: bool = DEFAULT_STAGE_6_QUIET_FFMPEG,
                 quiet_ffmpeg_final_video: bool = DEFAULT_QUIET_FFMPEG_FINAL_VIDEO):
        video_bits_folder = video_bits_folder.strip()

        self.video_bits_folder = video_bits_folder.removesuffix("/") if video_bits_folder.endswith("/") \
            else video_bits_folder
        self.overwrite_video_bits = overwrite_video_bits
        self.final_video_name = final_video_name.strip()
        self.presentation_duration = presentation_duration
        self.transition_duration = transition_duration
        self.transition_type = transition_type.strip()
        self.quiet_ffmpeg = quiet_ffmpeg
        self.quiet_ffmpeg_final_video = quiet_ffmpeg_final_video


@dataclass
class Config:
    start_from: Stage
    artifacts_folder: str
    stitch_final_video: bool
    stage_1: StageOneConfig
    stage_4: StageFourConfig
    stage_5: StageFiveConfig
    stage_6: StageSixConfig

    def __init__(self, start_from: Stage = DEFAULT_START_FROM_STAGE,
                 artifacts_folder: str = DEFAULT_ARTIFACTS_FOLDER,
                 stitch_final_video: bool = DEFAULT_STITCH_FINAL_VIDEO_FLAG,
                 stage_1: StageOneConfig = StageOneConfig(),
                 stage_4: StageFourConfig = StageFourConfig(),
                 stage_5: StageFiveConfig = StageFiveConfig(),
                 stage_6: StageSixConfig = StageSixConfig()):
        self.start_from = start_from
        self.artifacts_folder = artifacts_folder.strip()
        self.stitch_final_video = stitch_final_video
        self.stage_1 = stage_1
        self.stage_4 = stage_4
        self.stage_5 = stage_5
        self.stage_6 = stage_6
