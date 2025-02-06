import argparse

from peewee import PeeweeException

from common.type_definitions import StageException
from stage_6_final_video_bits_gen.defaults import DEFAULT_ARTIFACTS_FOLDER, DEFAULT_VIDEO_BITS_FOLDER, \
    DEFAULT_OVERWRITE_VIDEO_BITS, DEFAULT_QUIET_FFMPEG
from stage_6_final_video_bits_gen.execute import execute
from stage_6_final_video_bits_gen.stage_input import load_video_options_from_db

if __name__ == "__main__":

    # Configuration

    parser = argparse.ArgumentParser()
    parser.add_argument("--artifacts_folder", default=DEFAULT_ARTIFACTS_FOLDER)
    parser.add_argument("--video_bits_folder", default=DEFAULT_VIDEO_BITS_FOLDER)
    parser.add_argument("--overwrite_video_bits",
                        action=argparse.BooleanOptionalAction,
                        default=DEFAULT_OVERWRITE_VIDEO_BITS)
    parser.add_argument("--quiet_ffmpeg", action=argparse.BooleanOptionalAction,
                        default=DEFAULT_QUIET_FFMPEG)
    args = parser.parse_args()

    artifacts_folder_arg = args.artifacts_folder.strip()
    artifacts_folder = artifacts_folder_arg.removesuffix("/") if artifacts_folder_arg.endswith("/") \
        else artifacts_folder_arg

    video_bits_folder_arg = args.video_bits_folder.strip()
    video_bits_folder = video_bits_folder_arg.removesuffix("/") if video_bits_folder_arg.endswith("/") \
        else video_bits_folder_arg

    overwrite_video_bits = args.overwrite_video_bits
    quiet_ffmpeg = args.quiet_ffmpeg

    # Data retrieval

    try:
        video_options = load_video_options_from_db()
    except PeeweeException as err:
        print(f"[Stage 6 | Data retrieval] {err}")
        exit(1)

    # Execution

    try:
        result = execute(artifacts_folder=artifacts_folder,
                         video_bits_folder=video_bits_folder,
                         nominations_video_options=video_options,
                         overwrite=overwrite_video_bits,
                         quiet_ffmpeg=quiet_ffmpeg)
    except StageException as err:
        print(f"[Stage 6 | Execution] {err}")
        exit(1)

    # Execution feedback

    print("")
    print("[STAGE 6 SUMMARY | Final Video Bits Generation]")
    print(f"  # Loaded nominations: {len(video_options)}")
    print("")

    if result.nominations_missing_sources:
        print(f"  Nominations missing source files: ['{"', '".join(result.nominations_missing_sources)}']")
    print(f"  # Generated video bits: "
          f"{len(result.generated_video_bits_files) if result.generated_video_bits_files else 0}")

    if result.failed_video_bits:
        print(f"  Failed video bits: ['{"', '".join(result.failed_video_bits)}']")
