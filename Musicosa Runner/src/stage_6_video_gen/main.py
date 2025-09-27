import argparse

from peewee import PeeweeException

from common.config.loader import load_config
from common.custom_types import StageException
from stage_6_video_gen.custom_types import StageSixInput
from stage_6_video_gen.execute import execute
from stage_6_video_gen.stage_input import load_video_options_from_db
from stage_6_video_gen.summary import stage_summary

if __name__ == "__main__":
    # Configuration

    parser = argparse.ArgumentParser()
    parser.add_argument("--config_file")
    args = parser.parse_args()

    try:
        config = load_config(args.config_file.strip() if args.config_file else None)
    except FileNotFoundError | IOError | TypeError as err:
        print(f"[Stage 6 | Configuration] {err}")
        exit(1)

    stitch_final_video = config.stitch_final_video

    # Data retrieval

    try:
        video_options = load_video_options_from_db()
    except PeeweeException as err:
        print(f"[Stage 6 | Data retrieval] {err}")
        exit(1)

    stage_input = StageSixInput(video_options)

    # Execution

    try:
        result = execute(config, stage_input)
    except StageException as err:
        print(f"[Stage 6 | Execution] {err}")
        exit(1)

    # Stage execution summary

    print(stage_summary(config, stage_input, result))
