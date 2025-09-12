from enum import Flag, auto


class TemplateType(Flag):
    ENTRY = auto()
    PRESENTATION = auto()


class StageException(Exception):
    pass
