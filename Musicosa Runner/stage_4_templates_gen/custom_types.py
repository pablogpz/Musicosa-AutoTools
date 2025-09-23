from dataclasses import dataclass
from typing import NamedTuple

from common.custom_types import TemplateType


@dataclass
class Template:
    id: str
    entry_title: str
    types: TemplateType


class TemplateGenerationResult(NamedTuple):
    generated: list[str]
    skipped: list[str]
    failed: list[str]


@dataclass
class StageFourInput:
    templates: list[Template]


@dataclass
class StageFourOutput:
    entry_templates_result: TemplateGenerationResult
    presentation_templates_result: TemplateGenerationResult
