import argparse

from peewee import PeeweeException

from common.config.loader import load_config
from common.custom_types import StageException
from stage_4_templates_gen.custom_types import StageFourInput
from stage_4_templates_gen.execute import execute
from stage_4_templates_gen.stage_input import load_templates_from_db

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

    # Data retrieval

    try:
        templates = load_templates_from_db(generate_presentations=config.stitch_final_video)
    except PeeweeException as err:
        print(f"[Stage 4 | Data Retrieval] Failed to load templates UUIDs from database: {err}")
        exit(1)

    # Execution

    try:
        result = execute(config, StageFourInput(templates))
    except StageException as err:
        print(f"[Stage 4 | Execution] {err}")
        exit(1)

    # Execution feedback

    print("")
    print("[STAGE 4 SUMMARY | Templates Generation]")
    print(f"  # Templates to generate: {len(templates)}")
    print("")
    print(f"  # Successfully generated templates: "
          f"{len(result.generated_templates_slugs) if result.generated_templates_slugs else 0}")

    if result.failed_templates_uuids:
        print(f"  Failed to generate templates ['{"', '".join(result.failed_templates_uuids)}']")
