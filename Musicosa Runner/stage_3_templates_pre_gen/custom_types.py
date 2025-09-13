from dataclasses import dataclass

from common.model.models import Template, Setting, Nomination


@dataclass
class TFA:
    nominations_index_of_unfulfilled_templates: dict[int, Nomination]


@dataclass
class StageThreeInput:
    tfa: TFA


@dataclass
class StageThreeOutput:
    frame_settings: list[Setting] | None
    templates: list[Template] | None
