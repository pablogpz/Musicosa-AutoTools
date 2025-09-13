import os
from os import path
from typing import get_args

from common.custom_types import StageException
from stage_6_video_gen.custom_types import NominationVideoOptions, StageSixOutput, TransitionOptions, \
    TransitionType
from stage_6_video_gen.logic.generate_final_video import generate_final_video_collection
from stage_6_video_gen.logic.generate_video_bits import generate_video_bit_collection


def execute(artifacts_folder: str,
            video_bits_folder: str,
            nominations_video_options: list[NominationVideoOptions],
            overwrite: bool,
            stitch_final_video: bool,
            transition_options: TransitionOptions,
            quiet_ffmpeg: bool,
            quiet_ffmpeg_final_video: bool) -> StageSixOutput:
    if not artifacts_folder:
        raise StageException("No artifacts folder provided")

    if not path.isdir(artifacts_folder):
        raise StageException(f"Artifacts folder '{artifacts_folder}' not found")

    if not video_bits_folder:
        raise StageException("No video bits folder provided")

    if not path.isdir(video_bits_folder):
        os.makedirs(video_bits_folder)

    if transition_options.presentation_duration <= 0:
        raise StageException(
            f"presentation_duration ({transition_options.presentation_duration}) must be a positive integer")
    if transition_options.transition_duration <= 0:
        raise StageException(
            f"transition_duration ({transition_options.transition_duration}) must be a positive integer")
    if transition_options.type not in get_args(TransitionType):
        raise StageException(f"transition_type ({transition_options.type}) must be one of [{get_args(TransitionType)}]")

    if nominations_video_options is None:
        raise StageException("No video options provided")

    generated, missing_sources, failed_to_generate = (
        generate_video_bit_collection(artifacts_folder=artifacts_folder,
                                      video_bits_folder=video_bits_folder,
                                      overwrite=overwrite,
                                      quiet_ffmpeg=quiet_ffmpeg,
                                      nominations_video_options=nominations_video_options))

    award_final_video_paths = None

    if stitch_final_video:
        award_final_video_paths = generate_final_video_collection(artifacts_folder=artifacts_folder,
                                                                  video_bits_folder=video_bits_folder,
                                                                  quiet_ffmpeg=quiet_ffmpeg_final_video,
                                                                  vid_opts=nominations_video_options,
                                                                  transition_options=transition_options)

    return StageSixOutput(generated_video_bit_files=generated,
                          nominations_missing_sources=missing_sources,
                          failed_video_bits=failed_to_generate,
                          final_videos_files=award_final_video_paths)
