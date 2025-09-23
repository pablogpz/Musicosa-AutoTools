from enum import Flag, auto
from typing import Literal


class TemplateType(Flag):
    NOMINATION = auto()
    PRESENTATION = auto()


class StageException(Exception):
    pass


# Stage IDs

STAGE_ONE: Literal[1] = 1
STAGE_TWO: Literal[2] = 2
STAGE_THREE: Literal[3] = 3
STAGE_FOUR: Literal[4] = 4
STAGE_FIVE: Literal[5] = 5
STAGE_SIX: Literal[6] = 6

type Stage = Literal[1, 2, 3, 4, 5, 6]
