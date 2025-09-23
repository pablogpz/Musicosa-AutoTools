from dataclasses import dataclass
from typing import NamedTuple

from common.custom_types import TemplateType


@dataclass
class Template:
    id: str
    friendly_name: str
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
    nomination_templates_result: TemplateGenerationResult
    presentation_templates_result: TemplateGenerationResult
