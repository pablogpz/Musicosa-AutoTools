import { integer, primaryKey, real, sqliteTable, text } from 'drizzle-orm/sqlite-core'

import { MetadataFields, SettingGroupKeys, SettingNames, SettingValueType, SettingValueTypeSpec } from '@/db/models'

export const metadata = sqliteTable('metadata', {
    field: text('field').$type<MetadataFields>().primaryKey(),
    value: text('value').notNull(),
})

export const settings = sqliteTable(
    'settings',
    {
        groupKey: text('group_key').$type<SettingGroupKeys>().notNull(),
        setting: text('setting').$type<SettingNames>().notNull(),
        value: text('value').$type<SettingValueType>(),
        type: text('type').notNull().$type<SettingValueTypeSpec>().notNull().default('string'),
    },
    (table) => [primaryKey({ columns: [table.groupKey, table.setting] })]
)

export const avatars = sqliteTable('avatars', {
    id: integer('id').primaryKey({ autoIncrement: true }),
    imageFilename: text('image_filename').notNull(),
    imageHeight: real('image_height').notNull(),
    scoreBoxPositionTop: real('score_box_position_top').notNull(),
    scoreBoxPositionLeft: real('score_box_position_left').notNull(),
    scoreBoxFontScale: real('score_box_font_scale').notNull(),
    scoreBoxFontColor: text('score_box_font_color').notNull(),
})

export const members = sqliteTable('members', {
    id: text('id').primaryKey(),
    name: text('name').notNull().unique(),
    avatar: integer('avatar').references(() => avatars.id),
})

export const awards = sqliteTable('awards', {
    slug: text('slug').primaryKey(),
    designation: text('designation').notNull(),
})

export const nominations = sqliteTable('nominations', {
    id: text('id').primaryKey(),
    gameTitle: text('game_title').notNull(),
    nominee: text('nominee'),
    award: text('award')
        .references(() => awards.slug)
        .notNull(),
})

export const templates = sqliteTable('templates', {
    nomination: text('nomination')
        .references(() => nominations.id)
        .primaryKey(),
    avatarScale: real('avatar_scale').notNull(),
    videoBoxWidthPx: integer('video_box_width_px').notNull(),
    videoBoxHeightPx: integer('video_box_height_px').notNull(),
    videoBoxPositionTopPx: integer('video_box_position_top_px').notNull(),
    videoBoxPositionLeftPx: integer('video_box_position_left_px').notNull(),
})

export const videoclips = sqliteTable('videoclips', {
    id: integer('id').primaryKey(),
    url: text('url').notNull(),
})

export const videoOptions = sqliteTable('video_options', {
    nomination: text('nomination')
        .references(() => nominations.id)
        .primaryKey(),
    videoclip: integer('videoclip')
        .references(() => videoclips.id)
        .notNull(),
    timestampStart: text('timestamp_start').notNull(),
    timestampEnd: text('timestamp_end').notNull(),
})

export const castVotes = sqliteTable(
    'member_grades_nominations',
    {
        member: text('member').references(() => members.id),
        nomination: text('nomination')
            .references(() => nominations.id)
            .notNull(),
        score: real('score').notNull(),
    },
    (table) => [primaryKey({ columns: [table.member, table.nomination] })]
)

export const nominationStats = sqliteTable('stats_nominations', {
    nomination: text('nomination')
        .references(() => nominations.id)
        .primaryKey(),
    avgScore: real('avg_score'),
    rankingPlace: integer('ranking_place'),
    rankingSequence: integer('ranking_sequence'),
})
