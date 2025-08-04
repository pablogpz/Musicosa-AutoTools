import os
from os import path
from typing import get_args

from common.constants import VIDEO_FORMAT
from common.model.settings import is_setting_set
from common.type_definitions import StageException
from stage_6_final_video_bits_gen.logic.generate_final_video import generate_final_video
from stage_6_final_video_bits_gen.logic.generate_video_bits import generate_all_video_bits
from stage_6_final_video_bits_gen.type_definitions import EntryVideoOptions, StageSixOutput, TransitionOptions, \
    TransitionType


def execute(artifacts_folder: str,
            video_bits_folder: str,
            entries_video_options: list[EntryVideoOptions],
            overwrite: bool,
            stitch_final_video: bool,
            final_video_name: str,
            transition_options: TransitionOptions,
            quiet_ffmpeg: bool,
            quiet_ffmpeg_final_video: bool) -> StageSixOutput:
    if not is_setting_set("validation.entry_video_duration_seconds"):
        raise StageException("Setting 'validation.entry_video_duration_seconds' not set")

    if not is_setting_set("generation.videoclips_override_top_n_duration"):
        raise StageException("Setting 'generation.videoclips_override_top_n_duration' not set")

    if not is_setting_set("generation.videoclips_override_duration_up_to_x_seconds"):
        raise StageException("Setting 'generation.videoclips_override_duration_up_to_x_seconds' not set")

    if not artifacts_folder:
        raise StageException("No artifacts folder provided")

    if not path.isdir(artifacts_folder):
        raise StageException(f"Artifacts folder '{artifacts_folder}' not found")

    if not video_bits_folder:
        raise StageException("No video bits folder provided")

    if not path.isdir(video_bits_folder):
        os.makedirs(video_bits_folder)

    if entries_video_options is None or len(entries_video_options) == 0:
        raise StageException("No video options provided")

    if not final_video_name:
        raise StageException("No final video name provided")

    if transition_options.presentation_duration <= 0:
        raise StageException(
            f"presentation_duration ({transition_options.presentation_duration}) must be a positive integer")
    if transition_options.transition_duration <= 0:
        raise StageException(
            f"transition_duration ({transition_options.transition_duration}) must be a positive integer")
    if transition_options.type not in get_args(TransitionType):
        raise StageException(f"transition_type ({transition_options.type}) must be one of [{get_args(TransitionType)}]")

    generated, missing_sources, failed_to_generate = (
        generate_all_video_bits(artifacts_folder=artifacts_folder,
                                video_bits_folder=video_bits_folder,
                                overwrite=overwrite,
                                quiet_ffmpeg=quiet_ffmpeg,
                                entry_video_options=entries_video_options))

    final_video_path = None

    if stitch_final_video:
        existing_video_bits = [f"{video_bits_folder}/{entry.sequence_number}.{VIDEO_FORMAT}"
                               for entry in entries_video_options
                               if path.isfile(f"{video_bits_folder}/{entry.sequence_number}.{VIDEO_FORMAT}")]

        generated_or_existing_video_bits = {*(generated or []), *(existing_video_bits or [])}

        if len(entries_video_options) != len(generated_or_existing_video_bits):
            print(f"[SKIPPING FINAL VIDEO GENERATION] There are "
                  f"{len(entries_video_options) - len(generated_or_existing_video_bits)}"
                  f" missing video bits")
        else:
            final_video_path = generate_final_video(artifacts_folder=artifacts_folder,
                                                    video_bits_folder=video_bits_folder,
                                                    final_video_folder=video_bits_folder,
                                                    final_video_name=final_video_name,
                                                    quiet_ffmpeg=quiet_ffmpeg_final_video,
                                                    vid_opts=entries_video_options,
                                                    transition_options=transition_options)

    return StageSixOutput(generated_video_bits_files=generated,
                          entries_missing_sources=missing_sources,
                          failed_video_bits=failed_to_generate,
                          final_video=final_video_path)
