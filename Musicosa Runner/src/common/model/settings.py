from peewee import PeeweeException

from common.model.models import SETTING_KEY_SEPARATOR, Setting, SettingKeys


def get_setting_by_key(key: SettingKeys) -> Setting | None:
    key_bits = key.split(SETTING_KEY_SEPARATOR)

    if len(key_bits) != 2:
        raise ValueError(f"Invalid settings key '{key}'")

    group_key, setting = key_bits

    try:
        setting_entity = Setting.ORM.get((Setting.ORM.group_key == group_key) & (Setting.ORM.setting == setting))
    except PeeweeException as err:
        print(err)
        return None

    return setting_entity.to_domain()


def is_setting_set(key: SettingKeys) -> bool:
    setting = get_setting_by_key(key)

    return setting is not None and setting.value is not None
