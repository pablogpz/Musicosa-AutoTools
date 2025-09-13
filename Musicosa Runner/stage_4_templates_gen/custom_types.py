from dataclasses import dataclass

from common.custom_types import TemplateType
from stage_4_templates_gen.defaults import DEFAULT_OVERWRITE_TEMPLATES, \
    DEFAULT_OVERWRITE_PRESENTATIONS


@dataclass
class Template:
    uuid: str
    friendly_name: str
    template_targets: TemplateType


@dataclass
class StageFourInput:
    templates_api_url: str
    presentations_api_url: str
    artifacts_folder: str
    templates: list[Template]
    retry_attempts: int
    overwrite_templates: bool = DEFAULT_OVERWRITE_TEMPLATES
    overwrite_presentations: bool = DEFAULT_OVERWRITE_PRESENTATIONS


@dataclass
class StageFourOutput:
    generated_templates_slugs: list[str] | None
    failed_templates_uuids: list[str] | None
