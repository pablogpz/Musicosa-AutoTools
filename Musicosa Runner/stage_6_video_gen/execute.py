import os
from os import path
from typing import get_args, cast

from common.config.config import Config
from common.custom_types import StageException
from stage_6_video_gen.custom_types import StageSixOutput, StageSixInput, TransitionType, TransitionOptions
from stage_6_video_gen.logic.generate_final_video import generate_final_video_collection
from stage_6_video_gen.logic.generate_video_bits import generate_video_bit_collection


def execute(config: Config, stage_input: StageSixInput) -> StageSixOutput:
    artifacts_folder = config.artifacts_folder
    video_bits_folder = config.stage_6.video_bits_folder
    overwrite = config.stage_6.overwrite_video_bits
    stitch_final_video = config.stitch_final_video
    transition_options = TransitionOptions(config.stage_6.presentation_duration,
                                           config.stage_6.transition_duration,
                                           cast(TransitionType, config.stage_6.transition_type))
    quiet_ffmpeg = config.stage_6.quiet_ffmpeg
    quiet_ffmpeg_final_video = config.stage_6.quiet_ffmpeg_final_video
    nominations_video_options = stage_input.nominations_video_options

    if not artifacts_folder:
        raise StageException("No artifacts folder provided")

    if not path.isdir(artifacts_folder):
        raise StageException(f"Artifacts folder '{artifacts_folder}' not found")

    if not video_bits_folder:
        raise StageException("No video bits folder provided")

    if transition_options.presentation_duration <= 0:
        raise StageException(
            f"Presentation duration ({transition_options.presentation_duration}) must be a positive integer")

    if transition_options.transition_duration <= 0:
        raise StageException(
            f"Transition duration ({transition_options.transition_duration}) must be a positive integer")

    if transition_options.type not in get_args(TransitionType):
        raise StageException(f"Transition type ({transition_options.type}) must be one of [{get_args(TransitionType)}]")

    if nominations_video_options is None:
        raise StageException("No video options provided")

    if not path.isdir(video_bits_folder):
        os.makedirs(video_bits_folder)

    generated, missing_sources, failed_to_generate = generate_video_bit_collection(artifacts_folder,
                                                                                   video_bits_folder,
                                                                                   overwrite,
                                                                                   quiet_ffmpeg,
                                                                                   nominations_video_options)

    award_final_video_paths = None

    if stitch_final_video:
        award_final_video_paths = generate_final_video_collection(artifacts_folder,
                                                                  video_bits_folder,
                                                                  quiet_ffmpeg_final_video,
                                                                  nominations_video_options,
                                                                  transition_options)

    return StageSixOutput(generated, missing_sources, failed_to_generate, award_final_video_paths)
