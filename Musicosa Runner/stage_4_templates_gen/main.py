import argparse

from peewee import PeeweeException
from validators import url as validate_url, ValidationError

from common.types import StageException
from stage_4_templates_gen.defaults import DEFAULT_TEMPLATES_API_URL, DEFAULT_ARTIFACTS_FOLDER, \
    DEFAULT_GENERATION_RETRY_ATTEMPTS, DEFAULT_OVERWRITE_TEMPLATES, DEFAULT_PRESENTATIONS_API_URL, \
    DEFAULT_OVERWRITE_PRESENTATIONS, DEFAULT_GENERATE_PRESENTATIONS
from stage_4_templates_gen.execute import execute
from stage_4_templates_gen.stage_input import load_templates_from_db

if __name__ == "__main__":

    # Configuration

    parser = argparse.ArgumentParser()
    parser.add_argument("--templates_api_url", default=DEFAULT_TEMPLATES_API_URL)
    parser.add_argument("--presentations_api_url", default=DEFAULT_PRESENTATIONS_API_URL)
    parser.add_argument("--artifacts_folder", default=DEFAULT_ARTIFACTS_FOLDER)
    parser.add_argument("--generate_presentations",
                        action=argparse.BooleanOptionalAction,
                        default=DEFAULT_GENERATE_PRESENTATIONS)
    parser.add_argument("--gen_retry_attempts", type=int, default=DEFAULT_GENERATION_RETRY_ATTEMPTS)
    parser.add_argument("--overwrite_templates",
                        action=argparse.BooleanOptionalAction,
                        default=DEFAULT_OVERWRITE_TEMPLATES)
    parser.add_argument("--overwrite_presentations",
                        action=argparse.BooleanOptionalAction,
                        default=DEFAULT_OVERWRITE_PRESENTATIONS)
    args = parser.parse_args()

    templates_api_url_arg = args.templates_api_url.strip()
    templates_api_url = templates_api_url_arg.removesuffix("/") if templates_api_url_arg.endswith("/") \
        else templates_api_url_arg

    if isinstance(validate_url(templates_api_url, simple_host=True), ValidationError):
        print(f"[Stage 4 | Configuration] Invalid entry templates API URL '{templates_api_url}'")
        exit(1)

    presentations_api_url_arg = args.presentations_api_url.strip()
    presentations_api_url = presentations_api_url_arg.removesuffix("/") if presentations_api_url_arg.endswith("/") \
        else presentations_api_url_arg

    if isinstance(validate_url(presentations_api_url, simple_host=True), ValidationError):
        print(f"[Stage 4 | Configuration] Invalid presentation templates API URL '{presentations_api_url}'")
        exit(1)

    artifacts_folder_arg = args.artifacts_folder.strip()
    artifacts_folder = artifacts_folder_arg.removesuffix("/") if artifacts_folder_arg.endswith("/") \
        else artifacts_folder_arg

    generate_presentations = args.generate_presentations
    generation_retry_attempts = args.gen_retry_attempts
    overwrite_templates = args.overwrite_templates
    overwrite_presentations = args.overwrite_presentations

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
          f"{len(result.generated_templates) if result.generated_templates else 0}")
    if result.failed_templates_uuids:
        print(f"  Failed to generate templates ['{"', '".join(result.failed_templates_uuids)}']")
