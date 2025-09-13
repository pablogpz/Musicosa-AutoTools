import os
from os import path

from common.custom_types import StageException
from common.model.models import Videoclip
from stage_5_videoclips_acquisition.custom_types import StageFiveOutput
from stage_5_videoclips_acquisition.logic.download_videoclips import download_all_videoclips


def execute(artifacts_folder: str, quiet_ffmpeg: bool, videoclips: list[Videoclip]) -> StageFiveOutput:
    if not artifacts_folder:
        raise StageException("No artifacts folder provided")

    if not path.isdir(artifacts_folder):
        os.makedirs(artifacts_folder)

    if videoclips is None:
        raise StageException("No videoclips provided")

    acquired, failed_to_acquire = download_all_videoclips(videoclips=videoclips, artifacts_folder=artifacts_folder,
                                                          quiet_ffmpeg=quiet_ffmpeg)

    return StageFiveOutput(acquired_videoclip_titles=acquired, failed_videoclip_titles=failed_to_acquire)
