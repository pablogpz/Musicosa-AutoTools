import { NextRequest } from 'next/server'

import db from '@/db/database'
import {
    avatars,
    Contestant,
    contestants,
    contestantsStats,
    ContestantStats,
    entries,
    entriesStats,
    Entry,
    EntryStats,
    metadata,
    Scoring,
    scoring,
    settings,
    specialEntryTopics,
    Template,
    templates,
    videoOptions,
    VideoOptions
} from '@/db/schema'
import {
    mockAvatars,
    mockContestant,
    mockContestantStats,
    mockEntries,
    mockEntryStats,
    mockMetadata,
    mockScoring,
    mockSetting,
    mockSpecialEntryTopics,
    mockTemplate,
    mockVideoOption,
} from '@/db/mocks/schema'
import { RankingSettingsNames, SettingsGroups, TemplatesSettingsNames } from '@/db/settings'
import { MetadataFields } from '@/db/metadata'
import {
    DEFAULT_DECIMAL_DIGITS,
    DEFAULT_DISPLAY_DECIMAL_DIGITS,
    DEFAULT_TEMPLATE_HEIGHT,
    DEFAULT_TEMPLATE_WIDTH
} from '@/app/defaults'
import { Chance } from 'chance'

const DEFAULT_CONTESTANT_COUNT = 5
const DEFAULT_ENTRIES_COUNT = 10
const DEFAULT_SPECIAL_TOPICS_COUNT = 3

const chance = new Chance()

export async function GET(request: NextRequest) {
    const contestantsCount = parseInt(request.nextUrl.searchParams.get('contestants') ??
        DEFAULT_CONTESTANT_COUNT.toString())

    const entriesCount = parseInt(request.nextUrl.searchParams.get('entries') ??
        DEFAULT_ENTRIES_COUNT.toString())

    const metadataCollectionValues = Object.values(MetadataFields).map(field => mockMetadata({ field }))
    const settingsValues = [
        mockSetting({
            groupKey: SettingsGroups.ranking, setting: RankingSettingsNames.significantDecimalDigits,
            value: DEFAULT_DECIMAL_DIGITS, type: 'integer'
        }),
        mockSetting({
            groupKey: SettingsGroups.templates, setting: TemplatesSettingsNames.totalWidthPx,
            value: DEFAULT_TEMPLATE_WIDTH, type: 'integer'
        }),
        mockSetting({
            groupKey: SettingsGroups.templates, setting: TemplatesSettingsNames.totalHeightPx,
            value: DEFAULT_TEMPLATE_HEIGHT, type: 'integer'
        }),
        mockSetting({
            groupKey: SettingsGroups.templates, setting: TemplatesSettingsNames.displayDecimalDigits,
            value: DEFAULT_DISPLAY_DECIMAL_DIGITS, type: 'integer'
        }),
    ]
    const avatarsValues = mockAvatars(contestantsCount)
    const contestantsValues: Contestant[] = []
    avatarsValues.forEach(avatar => contestantsValues.push(mockContestant({ avatar: avatar.id })))
    const specialEntryTopicsValues = mockSpecialEntryTopics(DEFAULT_SPECIAL_TOPICS_COUNT)
    const entriesValues: Entry[] = []
    contestantsValues.forEach(contestant => {
        const specialTopicDesignationMock = chance.natural({ min: 1, max: 10 }) == 1 ?
            chance.pickone(specialEntryTopicsValues).designation : null

        const entryMocks = mockEntries(entriesCount, {
            author: contestant.id,
            specialTopic: specialTopicDesignationMock
        })

        entryMocks.forEach(entryMock => entriesValues.push({
            ...entryMock,
            specialTopic: specialTopicDesignationMock
        }))
    })
    const templatesValues: Template[] = []
    entriesValues.forEach(entry => templatesValues.push(mockTemplate({ entry: entry.id })))
    const videoOptionsValues: VideoOptions[] = []
    entriesValues.forEach(entry => videoOptionsValues.push(mockVideoOption({ entry: entry.id })))
    const scoringValues: Scoring[] = []
    contestantsValues
        .forEach(contestant => entriesValues
            .forEach(entry => scoringValues.push(mockScoring({ contestant: contestant.id, entry: entry.id }))))
    const contestantsStatsValues: ContestantStats[] = []
    contestantsValues
        .forEach(contestant => contestantsStatsValues.push(mockContestantStats({ contestant: contestant.id })))
    const entriesStatsValues: EntryStats[] = []
    entriesValues.forEach((entry, index) => entriesStatsValues.push(mockEntryStats({
        entry: entry.id,
        rankingSequence: index + 1
    })))

    try {
        await db.transaction(async tx => {
            try {
                await tx.insert(metadata).values(metadataCollectionValues).onConflictDoNothing()
                await tx.insert(settings).values(settingsValues).onConflictDoNothing()
                await tx.insert(avatars).values(avatarsValues).onConflictDoNothing()
                await tx.insert(contestants).values(contestantsValues).onConflictDoNothing()
                await tx.insert(specialEntryTopics).values(specialEntryTopicsValues).onConflictDoNothing()
                await tx.insert(entries).values(entriesValues).onConflictDoNothing()
                await tx.insert(templates).values(templatesValues).onConflictDoNothing()
                await tx.insert(videoOptions).values(videoOptionsValues).onConflictDoNothing()
                await tx.insert(scoring).values(scoringValues).onConflictDoNothing()
                await tx.insert(contestantsStats).values(contestantsStatsValues).onConflictDoNothing()
                await tx.insert(entriesStats).values(entriesStatsValues).onConflictDoNothing()
            } catch (sqliteError) {
                console.error(sqliteError)
                tx.rollback()
            }
        })
    } catch (txRolledBack) {
        return new Response("Mock data insertion failed")
    }

    return new Response("Success ✔")
}