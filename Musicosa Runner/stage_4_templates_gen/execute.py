import os
from os import path

from validators import url as validate_url, ValidationError

from common.custom_types import StageException
from common.model.models import SettingKeys
from common.model.settings import is_setting_set
from stage_4_templates_gen.constants import MAX_GEN_RETRY_ATTEMPTS
from stage_4_templates_gen.custom_types import Template, StageFourOutput
from stage_4_templates_gen.logic.generate_templates import generate_templates


def execute(templates_api_url: str,
            presentations_api_url: str,
            artifacts_folder: str,
            templates: list[Template],
            retry_attempts: int,
            overwrite_templates: bool,
            overwrite_presentations: bool) -> StageFourOutput:
    if not is_setting_set(SettingKeys.FRAME_WIDTH_PX):
        raise StageException(f"Setting '{SettingKeys.FRAME_WIDTH_PX}' not set")

    if not is_setting_set(SettingKeys.FRAME_HEIGHT_PX):
        raise StageException(f"Setting '{SettingKeys.FRAME_HEIGHT_PX}' not set")

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

    generated, failed_to_generate = generate_templates(templates_api_url=templates_api_url,
                                                       presentations_api_url=presentations_api_url,
                                                       templates=templates,
                                                       artifacts_folder=artifacts_folder,
                                                       retry_attempts=retry_attempts,
                                                       overwrite_templates=overwrite_templates,
                                                       overwrite_presentations=overwrite_presentations)

    return StageFourOutput(generated_templates_slugs=generated, failed_templates_uuids=failed_to_generate)
