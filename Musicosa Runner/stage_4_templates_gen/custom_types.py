from dataclasses import dataclass

from common.custom_types import TemplateType


@dataclass
class Template:
    uuid: str
    entry_title: str
    types: TemplateType


@dataclass
class StageFourInput:
    templates_api_url: str
    presentations_api_url: str
    artifacts_folder: str
    templates: list[Template]
    retry_attempts: int
    overwrite_templates: bool
    overwrite_presentations: bool


@dataclass
class StageFourOutput:
    generated_template_titles: list[str] | None
    failed_template_uuids: list[str] | None
