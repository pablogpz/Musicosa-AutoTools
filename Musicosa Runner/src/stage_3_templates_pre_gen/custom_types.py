from dataclasses import dataclass

from common.model.models import Nomination, Setting, Template


@dataclass
class TFA:
    nominations_index_unfulfilled_templates: dict[int, Nomination]


@dataclass
class StageThreeInput:
    tfa: TFA


@dataclass
class StageThreeOutput:
    frame_settings: list[Setting]
    templates: list[Template]
