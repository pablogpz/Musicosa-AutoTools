import os
from os import path

from validators import url as validate_url, ValidationError

from common.config.config import Config
from common.custom_types import StageException
from common.model.models import SettingKeys
from common.model.settings import is_setting_set
from stage_4_templates_gen.constants import MAX_GEN_RETRY_ATTEMPTS
from stage_4_templates_gen.custom_types import StageFourOutput, StageFourInput
from stage_4_templates_gen.logic.generate_templates import generate_templates


def execute(config: Config, stage_input: StageFourInput) -> StageFourOutput:
    templates_api_url = config.stage_4.templates_api_url
    presentations_api_url = config.stage_4.presentations_api_url
    artifacts_folder = config.artifacts_folder
    retry_attempts = config.stage_4.gen_retry_attempts
    overwrite_templates = config.stage_4.overwrite_templates
    overwrite_presentations = config.stage_4.overwrite_presentations
    templates = stage_input.templates

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
        raise StageException("No templates provided")

    if not (0 < retry_attempts <= MAX_GEN_RETRY_ATTEMPTS):
        raise StageException(
            f"Invalid retry attempts value '{retry_attempts}' (Should be between 1 and {MAX_GEN_RETRY_ATTEMPTS})")

    entry_templates, presentation_templates = generate_templates(templates_api_url,
                                                                 presentations_api_url,
                                                                 templates,
                                                                 artifacts_folder,
                                                                 retry_attempts,
                                                                 overwrite_templates,
                                                                 overwrite_presentations)

    return StageFourOutput(entry_templates, presentation_templates)
