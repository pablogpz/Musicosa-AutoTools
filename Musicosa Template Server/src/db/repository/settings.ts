import { and, eq, InferSelectModel, sql } from 'drizzle-orm'

import db from '@/db/database'
import { Setting, settings, SettingValueType, TypedSetting } from '@/db/schema'
import { SettingsGroups, SettingsKey } from '@/db/settings'
import { notInArray } from 'drizzle-orm/sql/expressions/conditions'

export interface SettingsRepository {
    getSettingByKey: <V extends SettingValueType>(settingKey: SettingsKey) => Promise<TypedSetting<V> | undefined>
    getSettingsGroup: (group: SettingsGroups) => Promise<Setting[] | undefined>
    getSettingsCollection: () => Promise<Setting[]>
}

let settingsCache: Setting[] = []

type RawSetting = InferSelectModel<typeof settings>

const parseSetting = (setting: RawSetting): Setting => ({
    ...setting, value:
        setting.type === 'integer' ? (setting?.value ? parseInt(setting.value as string) : setting?.value) :
            setting.type === 'real' ? (setting?.value ? parseFloat(setting.value as string) : setting?.value) :
                setting.type === 'boolean' ? (setting?.value ? Boolean((setting.value as string).toLowerCase()) : setting?.value) :
                    setting?.value
} as Setting)

const getSettingByKey = async <V extends SettingValueType>(settingKey: SettingsKey) => {
    const settingGroupKey = settingKey.split('.')[0]
    const settingName = settingKey.split('.')[1]

    const databaseQuery = db.select().from(settings)
        .where(
            and(
                eq(settings.groupKey, settingGroupKey),
                eq(settings.setting, settingName)
            ))
    let databaseResult

    if (process.env.NODE_ENV === "development") {
        databaseResult = await databaseQuery
        return databaseResult.length > 0 ? parseSetting(databaseResult[0]) as TypedSetting<V> : undefined
    }

    let settingCacheResult
    if ((settingCacheResult = settingsCache
        .find(setting =>
            setting.groupKey === settingGroupKey &&
            setting.setting === settingName)))
        return { ...settingCacheResult } as TypedSetting<V> // Careful: Shallow copy

    databaseResult = await databaseQuery

    let settingResult
    if (databaseResult.length > 0)
        settingsCache.push((settingResult = parseSetting(databaseResult[0])))

    return settingResult as TypedSetting<V>
}

const getSettingsGroup = async (group: SettingsGroups) => {
    const settingsGroupCache = settingsCache.filter(setting => setting.groupKey === group)

    const databaseQuery = db.select().from(settings).where(eq(settings.groupKey, group))

    if (process.env.NODE_ENV === "development")
        return databaseQuery as Promise<Setting[]>

    // CACHE MISS - EMPTY CACHE: Populate it from database if group exists
    if (settingsGroupCache.length === 0) {
        const settingsGroupDatabaseResult = await databaseQuery

        let settingsGroup
        if (settingsGroupDatabaseResult) {
            settingsCache.push(...(settingsGroup = settingsGroupDatabaseResult.map(parseSetting)))
            return settingsGroup.map(v => ({ ...v })) // Careful: Shallow copy
        }

        return undefined
    }

    const [{ settingsGroupSize }] = await db.select({
        settingsGroupSize: sql<number>`count(*)`,
    })
        .from(settings)
        .where(eq(settings.groupKey, group))

    // SETTINGS GROUP DOES NOT EXIST
    if (settingsGroupSize === 0) return undefined

    // PARTIAL CACHE HIT - SOME SETTINGS IN CACHE: Populate cache with missing settings
    if (settingsGroupCache.length < settingsGroupSize) {
        let missingSettings
        const missingSettingsResult = await db.select().from(settings)
            .where(
                and(
                    eq(settings.groupKey, group),
                    notInArray(settings.setting, settingsGroupCache.map(({ setting }) => setting))
                ))

        settingsCache.push(...(missingSettings = missingSettingsResult.map(parseSetting)))
        return missingSettings.map(v => ({ ...v })) // Careful: Shallow copy
    }

    // CACHE HIT - ALL SETTINGS IN CACHE
    if (settingsGroupCache.length === settingsGroupSize)
        return settingsGroupCache.map(v => ({ ...v })) // Careful: Shallow copy
}

const getSettingsCollection = async () => {
    const databaseQuery = db.select().from(settings)

    if (process.env.NODE_ENV === "development")
        return databaseQuery as Promise<Setting[]>

    if (settingsCache.length === 0) {
        const settingsCollectionResult = await databaseQuery
        if (settingsCollectionResult)
            settingsCache = settingsCollectionResult.map(parseSetting)
    }

    return settingsCache.map(v => ({ ...v })) // Careful: Shallow copy
}

const settingsRepository: SettingsRepository = {
    getSettingByKey,
    getSettingsGroup,
    getSettingsCollection
}

export default settingsRepository