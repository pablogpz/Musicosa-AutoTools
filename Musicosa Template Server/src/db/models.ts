import { InferSelectModel } from 'drizzle-orm'

import {
    avatars,
    awards,
    castVotes,
    members,
    metadata,
    nominationStats,
    nominations,
    settings,
    templates,
    videoOptions,
    videoclips,
} from '@/db/schema'

export type MetadataFields = 'edition' | 'topic' | 'organiser' | 'start_date'
export type Metadata = InferSelectModel<typeof metadata>

export type SettingGroupKeys = 'validation' | 'frame' | 'templates' | 'ranking'
export type ValidationSettingNames = 'score_min_value' | 'score_max_value'
export type FrameSettingNames = 'width_px' | 'height_px'
export type TemplatesSettingNames = 'display_decimal_digits'
export type RankingSettingNames = 'significant_decimal_digits'
export type SettingNames = ValidationSettingNames | FrameSettingNames | TemplatesSettingNames | RankingSettingNames
export type SettingValueType = number | string | boolean | null
export type SettingValueTypeSpec = 'integer' | 'real' | 'boolean' | 'string'
export const SETTING_KEY_SEPARATOR = '.'
export type SettingKeys =
    | `${Extract<SettingGroupKeys, 'validation'>}${typeof SETTING_KEY_SEPARATOR}${ValidationSettingNames}`
    | `${Extract<SettingGroupKeys, 'frame'>}${typeof SETTING_KEY_SEPARATOR}${FrameSettingNames}`
    | `${Extract<SettingGroupKeys, 'templates'>}${typeof SETTING_KEY_SEPARATOR}${TemplatesSettingNames}`
    | `${Extract<SettingGroupKeys, 'ranking'>}${typeof SETTING_KEY_SEPARATOR}${RankingSettingNames}`
export type Setting = InferSelectModel<typeof settings> &
    (
        | { groupKey: Extract<SettingGroupKeys, 'validation'>; setting: ValidationSettingNames }
        | { groupKey: Extract<SettingGroupKeys, 'frame'>; setting: FrameSettingNames }
        | { groupKey: Extract<SettingGroupKeys, 'templates'>; setting: TemplatesSettingNames }
        | { groupKey: Extract<SettingGroupKeys, 'ranking'>; setting: RankingSettingNames }
    ) &
    (
        | { type: 'integer' | 'real'; value: number | null }
        | { type: 'boolean'; value: boolean | null }
        | { type: 'string'; value: string | null }
    )
export type TypedSetting<T extends SettingValueType> = Omit<Setting, 'type'> & { value: T | null }

export type Avatar = InferSelectModel<typeof avatars>

export type Member = InferSelectModel<typeof members>

export type Award = InferSelectModel<typeof awards>

export type Nomination = InferSelectModel<typeof nominations>

export type Template = InferSelectModel<typeof templates>

export type Videoclip = InferSelectModel<typeof videoclips>

export type VideoOptions = InferSelectModel<typeof videoOptions>

export type CastVote = InferSelectModel<typeof castVotes>

export type NominationStats = InferSelectModel<typeof nominationStats>
