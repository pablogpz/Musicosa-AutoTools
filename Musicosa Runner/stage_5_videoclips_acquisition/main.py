import argparse

from peewee import PeeweeException

from common.config.loader import load_config
from common.custom_types import StageException
from stage_5_videoclips_acquisition.execute import execute
from stage_5_videoclips_acquisition.stage_input import load_videoclips_from_db

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
    quiet_ffmpeg = config.stage_5.quiet_ffmpeg

    # Data retrieval

    try:
        videoclips = load_videoclips_from_db()
    except PeeweeException as err:
        print(f"[Stage 5 | Data retrieval] {err}")
        exit(1)

    # Execution

    try:
        result = execute(artifacts_folder=artifacts_folder, quiet_ffmpeg=quiet_ffmpeg, videoclips=videoclips)
    except StageException as err:
        print(f"[Stage 5 | Execution] {err}")
        exit(1)

    # Execution feedback

    print("")
    print("[STAGE 5 SUMMARY | Videoclips Acquisition]")
    print(f"  # Videoclips: {len(videoclips)}")
    print("")
    print(
        f"  # Acquired videoclips: {len(result.acquired_videoclip_titles) if result.acquired_videoclip_titles else 0}")

    if result.failed_videoclip_titles:
        print(f"  Failed to acquire videoclips for: ['{"', '".join(result.failed_videoclip_titles)}']")
