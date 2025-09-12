import os
from os import path

from validators import url as validate_url, ValidationError

from common.model.settings import is_setting_set
from common.types import StageException
from stage_4_templates_gen.constants import MAX_GEN_RETRY_ATTEMPTS
from stage_4_templates_gen.logic.generate_templates import generate_all_templates
from stage_4_templates_gen.types import Template, StageFourOutput


def execute(
        templates_api_url: str,
        presentations_api_url: str,
        artifacts_folder: str,
        templates: list[Template],
        retry_attempts: int,
        overwrite_templates: bool,
        overwrite_presentations: bool,
) -> StageFourOutput:
    if not is_setting_set("frame.width_px"):
        raise StageException("Setting 'frame.width_px' not set")

    if not is_setting_set("frame.height_px"):
        raise StageException("Setting 'frame.height_px' not set")

    if isinstance(validate_url(templates_api_url, simple_host=True), ValidationError):
        raise StageException(f"Invalid entry templates API URL '{templates_api_url}'")

    if isinstance(validate_url(presentations_api_url, simple_host=True), ValidationError):
        raise StageException(f"Invalid presentation templates API URL '{presentations_api_url}'")

    if not artifacts_folder:
        raise StageException("No artifacts folder provided")

    if not path.isdir(artifacts_folder):
        os.makedirs(artifacts_folder)

    if templates is None:
        raise StageException("No templates UUIDs provided")

    if not (0 < retry_attempts <= MAX_GEN_RETRY_ATTEMPTS):
        raise StageException(
            f"Invalid retry attempts value '{retry_attempts}' (Should be between 1 and {MAX_GEN_RETRY_ATTEMPTS})")

    generated, failed_to_generate = generate_all_templates(templates_api_url=templates_api_url,
                                                           presentations_api_url=presentations_api_url,
                                                           templates=templates,
                                                           artifacts_folder=artifacts_folder,
                                                           retry_attempts=retry_attempts,
                                                           overwrite_templates=overwrite_templates,
                                                           overwrite_presentations=overwrite_presentations)

    return StageFourOutput(generated_templates_slugs=generated, failed_templates_uuids=failed_to_generate)
