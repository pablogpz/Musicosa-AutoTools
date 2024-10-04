import argparse

from peewee import PeeweeException
from validators import url as validate_url, ValidationError

from common.type_definitions import StageException
from stage_4_templates_gen.defaults import DEFAULT_TEMPLATES_API_URL, DEFAULT_ARTIFACTS_FOLDER, \
    DEFAULT_GENERATION_RETRY_ATTEMPTS, DEFAULT_OVERWRITE_TEMPLATES
from stage_4_templates_gen.execute import execute
from stage_4_templates_gen.stage_input import load_templates_from_db

if __name__ == "__main__":

    # Configuration

    parser = argparse.ArgumentParser()
    parser.add_argument("--api_url", default=DEFAULT_TEMPLATES_API_URL)
    parser.add_argument("--artifacts_folder", default=DEFAULT_ARTIFACTS_FOLDER)
    parser.add_argument("--gen_retry_attempts", type=int, default=DEFAULT_GENERATION_RETRY_ATTEMPTS)
    parser.add_argument("--overwrite_templates",
                        action=argparse.BooleanOptionalAction,
                        default=DEFAULT_OVERWRITE_TEMPLATES)
    args = parser.parse_args()

    api_url_arg = args.api_url.strip()
    api_url = api_url_arg.removesuffix("/") if api_url_arg.endswith("/") else api_url_arg

    if isinstance(validate_url(api_url, simple_host=True), ValidationError):
        print(f"[Stage 4 | Configuration] Invalid templates API URL '{api_url}'")
        exit(1)

    artifacts_folder_arg = args.artifacts_folder.strip()
    artifacts_folder = artifacts_folder_arg.removesuffix("/") if artifacts_folder_arg.endswith("/") \
        else artifacts_folder_arg

    generation_retry_attempts = args.gen_retry_attempts
    overwrite_templates = args.overwrite_templates

    # Data retrieval

    try:
        templates = load_templates_from_db()
    except PeeweeException as err:
        print(f"[Stage 4 | Data Retrieval] Failed to load templates UUIDs from database: {err}")
        exit(1)

    # Execution

    try:
        result = execute(templates_api_url=api_url,
                         artifacts_folder=artifacts_folder,
                         templates=templates,
                         retry_attempts=generation_retry_attempts,
                         overwrite=overwrite_templates)
    except StageException as err:
        print(f"[Stage 4 | Execution] {err}")
        exit(1)

    # Execution feedback

    print("")
    print("[STAGE 4 SUMMARY | Templates Generation]")
    print(f"  # Templates to generate: {len(templates)}")
    print("")
    print(f"  # Successfully generated templates: "
          f"{len(result.generated_templates) if result.generated_templates else 0}")
    if result.failed_templates_uuids:
        print(f"  Failed to generate templates ['{"', '".join(result.failed_templates_uuids)}']")
