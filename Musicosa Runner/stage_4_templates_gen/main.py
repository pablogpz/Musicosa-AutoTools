import argparse

from peewee import PeeweeException

from common.config.loader import load_config
from common.custom_types import StageException
from stage_4_templates_gen.custom_types import StageFourInput
from stage_4_templates_gen.execute import execute
from stage_4_templates_gen.stage_input import load_templates_from_db
from stage_4_templates_gen.summary import stage_summary

if __name__ == "__main__":

    # Configuration

    parser = argparse.ArgumentParser()
    parser.add_argument("--config_file")
    args = parser.parse_args()

    try:
        config = load_config(args.config_file.strip() if args.config_file else None)
    except FileNotFoundError | IOError | TypeError as err:
        print(f"[Stage 4 | Configuration] {err}")
        exit(1)

    # Data retrieval

    try:
        templates = load_templates_from_db(generate_presentations=config.stitch_final_video)
    except PeeweeException as err:
        print(f"[Stage 4 | Data Retrieval] {err}")
        exit(1)

    stage_input = StageFourInput(templates)

    # Execution

    try:
        result = execute(config, stage_input)
    except StageException as err:
        print(f"[Stage 4 | Execution] {err}")
        exit(1)

    # Stage execution summary

    print(stage_summary(config, stage_input, result))
