import argparse

from peewee import PeeweeException

from common.config.loader import load_config
from common.custom_types import StageException
from stage_6_video_gen.custom_types import TransitionOptions, TransitionType
from stage_6_video_gen.execute import execute
from stage_6_video_gen.stage_input import load_entries_video_options_from_db

if __name__ == "__main__":

    # Configuration

    parser = argparse.ArgumentParser()
    parser.add_argument("--config_file")
    args = parser.parse_args()

    try:
        config = load_config(args.config_file.strip() if args.config_file else None)
    except FileNotFoundError | IOError | TypeError as err:
        print(err)
        exit(1)

    artifacts_folder = config.artifacts_folder
    video_bits_folder = config.stage_6.video_bits_folder
    overwrite_video_bits = config.stage_6.overwrite_video_bits
    stitch_final_video = config.stitch_final_video
    final_video_name = config.stage_6.final_video_name
    presentation_duration = config.stage_6.presentation_duration
    transition_duration = config.stage_6.transition_duration
    transition_type = TransitionType(config.stage_6.transition_type)
    quiet_ffmpeg = config.stage_6.quiet_ffmpeg
    quiet_ffmpeg_final_video = config.stage_6.quiet_ffmpeg_final_video

    # Data retrieval

    try:
        entries_video_options = load_entries_video_options_from_db()
    except PeeweeException as err:
        print(f"[Stage 6 | Data retrieval] {err}")
        exit(1)

    # Execution

    try:
        result = execute(artifacts_folder=artifacts_folder,
                         video_bits_folder=video_bits_folder,
                         entries_video_options=entries_video_options,
                         overwrite=overwrite_video_bits,
                         stitch_final_video=stitch_final_video,
                         final_video_name=final_video_name,
                         transition_options=TransitionOptions(presentation_duration,
                                                              transition_duration,
                                                              transition_type),
                         quiet_ffmpeg=quiet_ffmpeg,
                         quiet_ffmpeg_final_video=quiet_ffmpeg_final_video)
    except StageException as err:
        print(f"[Stage 6 | Execution] {err}")
        exit(1)

    # Execution feedback

    print("")
    print("[STAGE 6 SUMMARY | Video Generation]")
    print(f"  # Loaded entries: {len(entries_video_options)}")
    print("")
    if result.entries_missing_sources:
        print(f"  Entries missing source files: ['{"', '".join(result.entries_missing_sources)}']")
    print(f"  # Generated video bits: "
          f"{len(result.generated_video_bit_files) if result.generated_video_bit_files else 0}")
    if result.failed_video_bits:
        print(f"  Failed video bits: ['{"', '".join(result.failed_video_bits)}']")
    if stitch_final_video:
        print(f"  Final video file: '{result.final_video_file}'")
