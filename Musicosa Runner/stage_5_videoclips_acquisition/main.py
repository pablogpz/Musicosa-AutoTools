import argparse

from peewee import PeeweeException

from common.config.loader import load_config
from common.custom_types import StageException
from stage_5_videoclips_acquisition.custom_types import StageFiveInput
from stage_5_videoclips_acquisition.execute import execute
from stage_5_videoclips_acquisition.stage_input import load_videoclips_from_db
from stage_5_videoclips_acquisition.summary import stage_summary

if __name__ == "__main__":

    # Configuration

    parser = argparse.ArgumentParser()
    parser.add_argument("--config_file")
    args = parser.parse_args()

    try:
        config = load_config(args.config_file.strip() if args.config_file else None)
    except FileNotFoundError | IOError | TypeError as err:
        print(f"[Stage 5 | Configuration] {err}")
        exit(1)

    # Data retrieval

    try:
        videoclips = load_videoclips_from_db()
    except PeeweeException as err:
        print(f"[Stage 5 | Data retrieval] {err}")
        exit(1)

    stage_input = StageFiveInput(videoclips)

    # Execution

    try:
        result = execute(config, stage_input)
    except StageException as err:
        print(f"[Stage 5 | Execution] {err}")
        exit(1)

    # Stage execution summary

    print(stage_summary(stage_input, result))
