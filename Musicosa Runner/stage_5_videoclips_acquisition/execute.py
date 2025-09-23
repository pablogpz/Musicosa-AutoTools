import os
from os import path, getenv

from common.config.config import Config
from common.custom_types import StageException
from stage_5_videoclips_acquisition.custom_types import StageFiveInput, StageFiveOutput
from stage_5_videoclips_acquisition.logic.download_videoclips import download_all_videoclips


def execute(config: Config, stage_input: StageFiveInput) -> StageFiveOutput:
    artifacts_folder, quiet_ffmpeg = (config.artifacts_folder, config.stage_5.quiet_ffmpeg)
    entries = stage_input.entries

    if not getenv("PATCHED_FFMPEG_PATH", ""):
        raise StageException("Patched FFmpeg path not set in environment variable 'PATCHED_FFMPEG_PATH'")

    if not artifacts_folder:
        raise StageException("No artifacts folder provided")

    if not path.isdir(artifacts_folder):
        os.makedirs(artifacts_folder)

    if entries is None:
        raise StageException("No entries provided")

    download_result = download_all_videoclips(entries, artifacts_folder, quiet_ffmpeg)

    return StageFiveOutput(download_result)
