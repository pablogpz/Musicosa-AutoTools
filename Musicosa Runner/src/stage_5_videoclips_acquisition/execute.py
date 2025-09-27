import os
from os import path, getenv

from common.config.config import Config
from common.custom_types import StageException
from stage_5_videoclips_acquisition.custom_types import StageFiveOutput, StageFiveInput
from stage_5_videoclips_acquisition.logic.download_videoclips import download_videoclips_collection


def execute(config: Config, stage_input: StageFiveInput) -> StageFiveOutput:
    artifacts_folder, use_cookies, quiet_ffmpeg = (
        config.artifacts_folder, config.stage_5.use_cookies, config.stage_5.quiet_ffmpeg)
    videoclips = stage_input.videoclips

    if not getenv("PATCHED_FFMPEG_PATH", ""):
        raise StageException("Patched FFmpeg path not set in environment variable 'PATCHED_FFMPEG_PATH'")

    if not artifacts_folder:
        raise StageException("No artifacts folder provided")

    if not path.isdir(artifacts_folder):
        os.makedirs(artifacts_folder)

    if videoclips is None:
        raise StageException("No videoclips provided")

    download_result = download_videoclips_collection(videoclips, artifacts_folder, use_cookies, quiet_ffmpeg)

    return StageFiveOutput(download_result)
