import argparse

from peewee import PeeweeException

from common.custom_types import StageException
from stage_5_videoclips_acquisition.defaults import DEFAULT_ARTIFACTS_FOLDER, DEFAULT_QUIET_FFMPEG
from stage_5_videoclips_acquisition.execute import execute
from stage_5_videoclips_acquisition.stage_input import load_entries_from_db

if __name__ == "__main__":

    # Configuration

    parser = argparse.ArgumentParser()
    parser.add_argument("--artifacts_folder", default=DEFAULT_ARTIFACTS_FOLDER)
    parser.add_argument("--quiet_ffmpeg", action=argparse.BooleanOptionalAction, default=DEFAULT_QUIET_FFMPEG)
    args = parser.parse_args()

    artifacts_folder_arg = args.artifacts_folder.strip()
    artifacts_folder = artifacts_folder_arg.removesuffix("/") if artifacts_folder_arg.endswith("/") \
        else artifacts_folder_arg

    quiet_ffmpeg = args.quiet_ffmpeg

    # Data retrieval

    try:
        entries = load_entries_from_db()
    except PeeweeException as err:
        print(f"[Stage 5 | Data retrieval] {err}")
        exit(1)

    # Execution

    try:
        result = execute(artifacts_folder=artifacts_folder, quiet_ffmpeg=quiet_ffmpeg, entries=entries)
    except StageException as err:
        print(f"[Stage 5 | Execution] {err}")
        exit(1)

    # Execution feedback

    print("")
    print("[STAGE 5 SUMMARY | Videoclips Acquisition]")
    print(f"  # Entries: {len(entries)}")
    print("")
    print(f"  # Acquired videoclips: {len(result.acquired_videoclips) if result.acquired_videoclips else 0}")
    if result.failed_to_acquire:
        print(f"  Failed to acquire videoclips for: ['{"', '".join(result.failed_to_acquire)}']")
