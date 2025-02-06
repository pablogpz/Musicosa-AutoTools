import os
from os import path

from common.model.models import Videoclip
from common.type_definitions import StageException
from stage_5_videoclips_acquisition.logic.download_videoclips import download_all_videoclips
from stage_5_videoclips_acquisition.type_definitions import StageFiveOutput


def execute(artifacts_folder: str, quiet_ffmpeg: bool, videoclips: list[Videoclip]) -> StageFiveOutput:
    if not artifacts_folder:
        raise StageException("No artifacts folder provided")

    if not path.isdir(artifacts_folder):
        os.makedirs(artifacts_folder)

    if videoclips is None:
        raise StageException("No videoclips provided")

    acquired, failed_to_acquire = download_all_videoclips(videoclips=videoclips, artifacts_folder=artifacts_folder,
                                                          quiet_ffmpeg=quiet_ffmpeg)

    return StageFiveOutput(acquired_videoclips=acquired, failed_to_acquire=failed_to_acquire)
