import argparse
from typing import get_args

from peewee import PeeweeException

from common.custom_types import StageException
from stage_6_video_gen.custom_types import TransitionOptions, TransitionType
from stage_6_video_gen.defaults import DEFAULT_ARTIFACTS_FOLDER, DEFAULT_VIDEO_BITS_FOLDER, \
    DEFAULT_FINAL_VIDEO_NAME, DEFAULT_STITCH_FINAL_VIDEO_FLAG, DEFAULT_OVERWRITE_VIDEO_BITS, DEFAULT_QUIET_FFMPEG, \
    DEFAULT_QUIET_FFMPEG_FINAL_VIDEO, DEFAULT_TRANSITION_DURATION, DEFAULT_PRESENTATION_DURATION, \
    DEFAULT_TRANSITION_TYPE
from stage_6_video_gen.execute import execute
from stage_6_video_gen.stage_input import load_entries_video_options_from_db

if __name__ == "__main__":

    # Configuration

    parser = argparse.ArgumentParser()
    parser.add_argument("--artifacts_folder", default=DEFAULT_ARTIFACTS_FOLDER)
    parser.add_argument("--video_bits_folder", default=DEFAULT_VIDEO_BITS_FOLDER)
    parser.add_argument("--overwrite_video_bits",
                        action=argparse.BooleanOptionalAction,
                        default=DEFAULT_OVERWRITE_VIDEO_BITS)
    parser.add_argument("--final_video",
                        action=argparse.BooleanOptionalAction,
                        default=DEFAULT_STITCH_FINAL_VIDEO_FLAG)
    parser.add_argument("--final_video_name", default=DEFAULT_FINAL_VIDEO_NAME)
    parser.add_argument("--presentation_duration", default=DEFAULT_PRESENTATION_DURATION)
    parser.add_argument("--transition_duration", default=DEFAULT_TRANSITION_DURATION)
    parser.add_argument("--transition_type", default=DEFAULT_TRANSITION_TYPE)
    parser.add_argument("--quiet_ffmpeg", action=argparse.BooleanOptionalAction,
                        default=DEFAULT_QUIET_FFMPEG)
    parser.add_argument("--quiet_ffmpeg_final_video", action=argparse.BooleanOptionalAction,
                        default=DEFAULT_QUIET_FFMPEG_FINAL_VIDEO)
    args = parser.parse_args()

    artifacts_folder_arg = args.artifacts_folder.strip()
    artifacts_folder = artifacts_folder_arg.removesuffix("/") if artifacts_folder_arg.endswith("/") \
        else artifacts_folder_arg

    video_bits_folder_arg = args.video_bits_folder.strip()
    video_bits_folder = video_bits_folder_arg.removesuffix("/") if video_bits_folder_arg.endswith("/") \
        else video_bits_folder_arg

    overwrite_video_bits = args.overwrite_video_bits
    final_video = args.final_video
    final_video_name = args.final_video_name.strip()

    presentation_duration = int(args.presentation_duration)
    if presentation_duration <= 0:
        print(f"[Stage 6 | Configuration] presentation_duration ({presentation_duration}) must be a positive integer")
    transition_duration = int(args.transition_duration)
    if transition_duration <= 0:
        print(f"[Stage 6 | Configuration] transition_duration ({transition_duration}) must be a positive integer")
    transition_type = args.transition_type.strip()
    if transition_type not in get_args(TransitionType):
        print(f"[Stage 6 | Configuration] "
              f"transition_type ({transition_type}) must be one of [{get_args(TransitionType)}]")
    transition_options: TransitionOptions = TransitionOptions(presentation_duration,
                                                              transition_duration,
                                                              transition_type)

    quiet_ffmpeg = args.quiet_ffmpeg
    quiet_ffmpeg_final_video = args.quiet_ffmpeg_final_video

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
                         stitch_final_video=final_video,
                         final_video_name=final_video_name,
                         transition_options=transition_options,
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
    if final_video:
        print(f"  Final video file: '{result.final_video_file}'")
