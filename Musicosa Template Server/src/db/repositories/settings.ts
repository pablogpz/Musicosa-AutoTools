import { InferSelectModel, and, eq } from 'drizzle-orm'

import db from '@/db/database'
import {
    SETTING_KEY_SEPARATOR,
    Setting,
    SettingGroupKeys,
    SettingKeys,
    SettingNames,
    SettingValueType,
    TypedSetting,
} from '@/db/models'
import { settings } from '@/db/schema'

export interface SettingsRepository {
    getSettingByKey: <V extends SettingValueType>(settingKey: SettingKeys) => Promise<TypedSetting<V> | undefined>
}

const settingsCache: Map<SettingKeys, Setting> = new Map()

type RawSetting = InferSelectModel<typeof settings>

const parseSettingResult = (setting: RawSetting): Setting =>
    ({
        ...setting,
        value:
            setting.type === 'integer'
                ? setting?.value
                    ? parseInt(setting.value as string)
                    : null
                : setting.type === 'real'
                  ? setting?.value
                      ? parseFloat(setting.value as string)
                      : null
                  : setting.type === 'boolean'
                    ? setting?.value
                        ? Boolean((setting.value as string).toLowerCase())
                        : null
                    : (setting?.value ?? null),
    }) as Setting

const getSettingByKey = async <V extends SettingValueType>(
    settingKey: SettingKeys
): Promise<TypedSetting<V> | undefined> => {
    if (process.env.NODE_ENV === 'development' || !settingsCache.has(settingKey)) {
        const [settingGroupKey, settingName] = settingKey.split(SETTING_KEY_SEPARATOR) as [
            SettingGroupKeys,
            SettingNames,
        ]

        const result = await db
            .select()
            .from(settings)
            .where(and(eq(settings.groupKey, settingGroupKey), eq(settings.setting, settingName)))

        if (result.length == 0) return undefined

        settingsCache.set(settingKey, parseSettingResult(result[0]))
    }

    return structuredClone(settingsCache.get(settingKey)) as TypedSetting<V>
}

const settingsRepository: SettingsRepository = { getSettingByKey }

export default settingsRepository
