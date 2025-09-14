import argparse

from peewee import PeeweeException

from common.config.loader import load_config
from common.custom_types import StageException
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

    generate_presentations = config.stitch_final_video
    templates_api_url = config.stage_4.templates_api_url
    presentations_api_url = config.stage_4.presentations_api_url
    artifacts_folder = config.artifacts_folder
    generation_retry_attempts = config.stage_4.gen_retry_attempts
    overwrite_templates = config.stage_4.overwrite_templates
    overwrite_presentations = config.stage_4.overwrite_presentations

    # Data retrieval

    try:
        templates = load_templates_from_db(generate_presentations)
    except PeeweeException as err:
        print(f"[Stage 4 | Data Retrieval] Failed to load templates UUIDs from database: {err}")
        exit(1)

    # Execution

    try:
        result = execute(templates_api_url=templates_api_url,
                         presentations_api_url=presentations_api_url,
                         artifacts_folder=artifacts_folder,
                         templates=templates,
                         retry_attempts=generation_retry_attempts,
                         overwrite_templates=overwrite_templates,
                         overwrite_presentations=overwrite_presentations)
    except StageException as err:
        print(f"[Stage 4 | Execution] {err}")
        exit(1)

    # Execution feedback

    print("")
    print("[STAGE 4 SUMMARY | Templates Generation]")
    print(f"  # Templates to generate: {len(templates)}")
    print("")
    print(f"  # Successfully generated templates: "
          f"{len(result.generated_template_titles) if result.generated_template_titles else 0}")
    if result.failed_template_uuids:
        print(f"  Failed to generate templates ['{"', '".join(result.failed_template_uuids)}']")
