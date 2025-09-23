import os
from os import path
from typing import get_args, cast

from common.config.config import Config
from common.custom_types import StageException
from common.model.models import SettingKeys
from common.model.settings import is_setting_set
from stage_6_video_gen.custom_types import TransitionOptions, StageSixInput, StageSixOutput, TransitionType
from stage_6_video_gen.logic.generate_final_video import generate_final_video
from stage_6_video_gen.logic.generate_video_bits import generate_video_bit_collection


def execute(config: Config, stage_input: StageSixInput) -> StageSixOutput:
    artifacts_folder = config.artifacts_folder
    video_bits_folder = config.stage_6.video_bits_folder
    overwrite = config.stage_6.overwrite_video_bits
    stitch_final_video = config.stitch_final_video
    final_video_name = config.stage_6.final_video_name
    transition_options = TransitionOptions(config.stage_6.presentation_duration,
                                           config.stage_6.transition_duration,
                                           cast(TransitionType, config.stage_6.transition_type))
    quiet_ffmpeg = config.stage_6.quiet_ffmpeg
    quiet_ffmpeg_final_video = config.stage_6.quiet_ffmpeg_final_video
    entries_video_options = stage_input.entries_video_options

    final_video_path = None

    if not is_setting_set(SettingKeys.VALIDATION_ENTRY_VIDEO_DURATION_SECONDS):
        raise StageException(f"Setting '{SettingKeys.VALIDATION_ENTRY_VIDEO_DURATION_SECONDS}' not set")

    if not is_setting_set(SettingKeys.GENERATION_VIDEOCLIPS_OVERRIDE_TOP_N_DURATION):
        raise StageException(f"Setting '{SettingKeys.GENERATION_VIDEOCLIPS_OVERRIDE_TOP_N_DURATION}' not set")

    if not is_setting_set(SettingKeys.GENERATION_VIDEOCLIPS_OVERRIDE_DURATION_UP_TO_X_SECONDS):
        raise StageException(f"Setting '{SettingKeys.GENERATION_VIDEOCLIPS_OVERRIDE_DURATION_UP_TO_X_SECONDS}' not set")

    if not artifacts_folder:
        raise StageException("No artifacts folder provided")

    if not path.isdir(artifacts_folder):
        raise StageException(f"Artifacts folder '{artifacts_folder}' not found")

    if not video_bits_folder:
        raise StageException("No video bits folder provided")

    if entries_video_options is None or len(entries_video_options) == 0:
        raise StageException("No video options provided")

    if not final_video_name:
        raise StageException("No final video name provided")

    if transition_options.presentation_duration <= 0:
        raise StageException(
            f"Presentation duration ({transition_options.presentation_duration}) must be a positive integer")

    if transition_options.transition_duration <= 0:
        raise StageException(
            f"Transition duration ({transition_options.transition_duration}) must be a positive integer")

    if transition_options.type not in get_args(TransitionType):
        raise StageException(f"Transition type ({transition_options.type}) must be one of [{get_args(TransitionType)}]")

    if not path.isdir(video_bits_folder):
        os.makedirs(video_bits_folder)

    missing_templates, missing_videoclips, generation_result = (
        generate_video_bit_collection(artifacts_folder, video_bits_folder, overwrite, quiet_ffmpeg,
                                      entries_video_options))
    generated, skipped, _failed = generation_result

    if stitch_final_video:
        existing_video_bit_count = len(generated) + len(skipped)

        if len(entries_video_options) != existing_video_bit_count:
            print(f"[SKIPPING FINAL VIDEO GENERATION] There are "
                  f"{len(entries_video_options) - existing_video_bit_count}"
                  f" missing video bits")
        else:
            final_video_path = generate_final_video(artifacts_folder,
                                                    video_bits_folder,
                                                    video_bits_folder,
                                                    final_video_name,
                                                    quiet_ffmpeg_final_video,
                                                    entries_video_options,
                                                    transition_options)

    return StageSixOutput(missing_templates, missing_videoclips, generation_result, final_video_path)
