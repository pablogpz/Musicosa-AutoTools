from enum import Enum
from typing import Literal

from peewee import PeeweeException

from common.model.models import Setting


class SettingsGroups(Enum):
    VALIDATION = "validation"
    RANKING = "ranking"
    TEMPLATES = "templates"


class ValidationSettingsNames(Enum):
    SCORE_MIN_VALUE = "score_min_value"
    SCORE_MAX_VALUE = "score_max_value"


class RankingSettingsNames(Enum):
    SIGNIFICANT_DECIMAL_DIGITS = "significant_decimal_digits"


class TemplateSettingsNames(Enum):
    TOTAL_WIDTH_PX = "total_width_px"
    TOTAL_HEIGHT_PX = "total_height_px"


type SettingsKeys = Literal[
    "validation.score_min_value",
    "validation.score_max_value",
    "ranking.significant_decimal_digits",
    "templates.total_width_px",
    "templates.total_height_px",
]


def get_setting_by_key(key: SettingsKeys) -> Setting | None:
    key_bits = key.split(".")

    if len(key_bits) != 2:
        raise ValueError(f"Invalid settings key '{key}'")

    group_key, setting = key_bits

    try:
        setting_entity = Setting.ORM.get((Setting.ORM.group_key == group_key) & (Setting.ORM.setting == setting))
    except PeeweeException as err:
        print(err)
        return None

    return setting_entity.to_domain()


def is_setting_set(key: SettingsKeys) -> bool:
    setting = get_setting_by_key(key)

    return setting is not None and setting.value is not None
