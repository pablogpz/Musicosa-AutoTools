from dataclasses import dataclass

from common.custom_types import TemplateType


@dataclass
class Template:
    uuid: str
    entry_title: str
    types: TemplateType


@dataclass
class StageFourInput:
    templates: list[Template]


@dataclass
class StageFourOutput:
    generated_template_titles: list[str] | None
    failed_template_uuids: list[str] | None
