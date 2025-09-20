import os
from os import path, getenv

from common.custom_types import StageException
from common.model.models import Entry
from stage_5_videoclips_acquisition.custom_types import StageFiveOutput
from stage_5_videoclips_acquisition.logic.download_videoclips import download_all_videoclips


def execute(artifacts_folder: str, quiet_ffmpeg: bool, entries: list[Entry]) -> StageFiveOutput:
    if not getenv("PATCHED_FFMPEG_PATH", ""):
        raise StageException("Patched FFmpeg path not set in environment variable 'PATCHED_FFMPEG_PATH'")

    if not artifacts_folder:
        raise StageException("No artifacts folder provided")

    if not path.isdir(artifacts_folder):
        os.makedirs(artifacts_folder)

    if entries is None:
        raise StageException("No entries provided")

    acquired, failed_to_acquire = download_all_videoclips(entries, artifacts_folder, quiet_ffmpeg)

    return StageFiveOutput(acquired, failed_to_acquire)
