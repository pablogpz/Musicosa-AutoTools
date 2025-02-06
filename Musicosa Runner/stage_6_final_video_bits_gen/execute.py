import os
from os import path

from common.type_definitions import StageException
from stage_6_final_video_bits_gen.logic.generate_video_bits import generate_all_video_bits
from stage_6_final_video_bits_gen.type_definitions import NominationVideoOptions, StageSixOutput


def execute(artifacts_folder: str,
            video_bits_folder: str,
            nominations_video_options: list[NominationVideoOptions],
            overwrite: bool,
            quiet_ffmpeg: bool) -> StageSixOutput:
    if not artifacts_folder:
        raise StageException("No artifacts folder provided")

    if not path.isdir(artifacts_folder):
        raise StageException(f"Artifacts folder '{artifacts_folder}' not found")

    if not video_bits_folder:
        raise StageException("No video bits folder provided")

    if not path.isdir(video_bits_folder):
        os.makedirs(video_bits_folder)

    if nominations_video_options is None:
        raise StageException("No video options provided")

    generated, missing_sources, failed_to_generate = (
        generate_all_video_bits(artifacts_folder=artifacts_folder,
                                video_bits_folder=video_bits_folder,
                                overwrite=overwrite,
                                quiet_ffmpeg=quiet_ffmpeg,
                                nominations_video_options=nominations_video_options))

    return StageSixOutput(generated_video_bits_files=generated,
                          nominations_missing_sources=missing_sources,
                          failed_video_bits=failed_to_generate)
