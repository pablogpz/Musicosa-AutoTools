from dataclasses import dataclass

from common.custom_types import TemplateType


@dataclass
class Template:
    id: str
    friendly_name: str
    types: TemplateType


@dataclass
class StageFourInput:
    templates: list[Template]


@dataclass
class StageFourOutput:
    generated_templates_slugs: list[str]
    failed_templates_ids: list[str]
