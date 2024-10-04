import { integer, primaryKey, real, sqliteTable, text } from 'drizzle-orm/sqlite-core'
import { InferSelectModel } from 'drizzle-orm'

export const metadata = sqliteTable('metadata', {
    field: text('field').primaryKey(),
    value: text('value').notNull()
})
export type Metadata = InferSelectModel<typeof metadata>

export const settings = sqliteTable('settings', {
    groupKey: text('group_key').notNull(),
    setting: text('setting').notNull(),
    value: text('value').$type<SettingValueType>(),
    type: text('type').notNull().$type<SettingValueTypeSpec>().default('string')
}, (table) => ({
    pk: primaryKey({ columns: [table.groupKey, table.setting] })
}))
export type SettingValueType = number | string | boolean
export type SettingValueTypeSpec = 'integer' | 'real' | 'string' | 'boolean'
export type Setting = InferSelectModel<typeof settings> & (
    { type: 'integer' | 'real', value: number | null } |
    { type: 'boolean', value: boolean | null } |
    { type: 'string', value: string | null })
export type TypedSetting<T extends SettingValueType> = Omit<Setting, 'type'> & { value: T | null }

export const avatars = sqliteTable('avatars', {
    id: integer('id').primaryKey({ autoIncrement: true }),
    imageFilename: text('image_filename').notNull(),
    imageHeight: real('image_height').notNull(),
    scoreBoxPositionTop: real('score_box_position_top').notNull(),
    scoreBoxPositionLeft: real('score_box_position_left').notNull(),
    scoreBoxFontScale: real('score_box_font_scale').notNull(),
    scoreBoxFontColor: text('score_box_font_color')
})
export type Avatar = InferSelectModel<typeof avatars>

export const contestants = sqliteTable('contestants', {
    id: text('id').primaryKey(),
    name: text('name').notNull(),
    avatar: integer('avatar').references(() => avatars.id)
})
export type Contestant = InferSelectModel<typeof contestants>

export const specialEntryTopics = sqliteTable('special_entry_topics', {
    designation: text('designation').primaryKey()
})
export type SpecialEntryTopic = InferSelectModel<typeof specialEntryTopics>

export const entries = sqliteTable('entries', {
    id: text('id').primaryKey(),
    title: text('title').notNull().unique(),
    author: text('author').references(() => contestants.id),
    videoUrl: text('video_url').notNull(),
    specialTopic: text('special_topic').references(() => specialEntryTopics.designation)
})
export type Entry = InferSelectModel<typeof entries>

export const templates = sqliteTable('templates', {
    entry: text('entry').references(() => entries.id).primaryKey(),
    avatarScale: real('avatar_scale').notNull(),
    videoBoxWidthPx: integer('video_box_width_px').notNull(),
    videoBoxHeightPx: integer('video_box_height_px').notNull(),
    videoBoxPositionTopPx: integer('video_box_position_top_px').notNull(),
    videoBoxPositionLeftPx: integer('video_box_position_left_px').notNull(),
})
export type Template = InferSelectModel<typeof templates>

export const videoOptions = sqliteTable('video_options', {
    entry: text('entry').references(() => entries.id).primaryKey(),
    timestampStart: text('timestamp_start'),
    timestampEnd: text('timestamp_end'),
})
export type VideoOptions = InferSelectModel<typeof videoOptions>

export const scoring = sqliteTable('contestant_grades_entries', {
    contestant: text('contestant').references(() => contestants.id),
    entry: text('entry').references(() => entries.id).notNull(),
    score: real('score').notNull()
}, (table) => ({
    pk: primaryKey({ columns: [table.contestant, table.entry] })
}))
export type Scoring = InferSelectModel<typeof scoring>

export const contestantsStats = sqliteTable('stats_contestants', {
    contestant: text('contestant').references(() => contestants.id).primaryKey(),
    avgScore: real('avg_score'),
})
export type ContestantStats = InferSelectModel<typeof contestantsStats>

export const entriesStats = sqliteTable('stats_entries', {
    entry: text('entry').references(() => entries.id).primaryKey(),
    avgScore: real('avg_score'),
    rankingPlace: integer('ranking_place'),
    rankingSequence: integer('ranking_sequence').unique(),
})
export type EntryStats = InferSelectModel<typeof entriesStats>