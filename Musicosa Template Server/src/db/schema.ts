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

export const contestants = sqliteTable('contestants', {
    id: text('id').primaryKey(),
    name: text('name').notNull().unique(),
    avatar: integer('avatar').references(() => avatars.id),
})

export const entryTopics = sqliteTable('entry_topics', {
    designation: text('designation').primaryKey(),
})

export const entries = sqliteTable('entries', {
    id: text('id').primaryKey(),
    title: text('title').notNull().unique(),
    author: text('author').references(() => contestants.id),
    videoUrl: text('video_url').notNull(),
    topic: text('topic').references(() => entryTopics.designation),
})

export const templates = sqliteTable('templates', {
    entry: text('entry')
        .references(() => entries.id)
        .primaryKey(),
    avatarScale: real('avatar_scale').notNull(),
    authorAvatarScale: real('author_avatar_scale').notNull(),
    videoBoxWidthPx: integer('video_box_width_px').notNull(),
    videoBoxHeightPx: integer('video_box_height_px').notNull(),
    videoBoxPositionTopPx: integer('video_box_position_top_px').notNull(),
    videoBoxPositionLeftPx: integer('video_box_position_left_px').notNull(),
})

export const videoOptions = sqliteTable('video_options', {
    entry: text('entry')
        .references(() => entries.id)
        .primaryKey(),
    timestampStart: text('timestamp_start').notNull(),
    timestampEnd: text('timestamp_end').notNull(),
})

export const scoring = sqliteTable(
    'contestant_grades_entries',
    {
        contestant: text('contestant').references(() => contestants.id),
        entry: text('entry')
            .references(() => entries.id)
            .notNull(),
        score: real('score').notNull(),
    },
    (table) => [primaryKey({ columns: [table.contestant, table.entry] })]
)

export const contestantsStats = sqliteTable('stats_contestants', {
    contestant: text('contestant')
        .references(() => contestants.id)
        .primaryKey(),
    avgGivenScore: real('avg_given_score'),
    avgReceivedScore: real('avg_received_score'),
})

export const entriesStats = sqliteTable('stats_entries', {
    entry: text('entry')
        .references(() => entries.id)
        .primaryKey(),
    avgScore: real('avg_score'),
    rankingPlace: integer('ranking_place'),
    rankingSequence: integer('ranking_sequence').unique(),
})
