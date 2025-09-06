import { Chance } from 'chance'

import {
    Avatar,
    Contestant,
    ContestantStats,
    Entry,
    EntryStats,
    Metadata,
    MetadataFields,
    Scoring,
    Setting,
    SpecialEntryTopic,
    Template,
    VideoOptions
} from '@/db/models'

const chance = new Chance()

const metadataFieldNames: MetadataFields[] = ['edition', 'topic', 'organiser', 'start_date']
export const mockMetadata = (partial?: Partial<Metadata>): Metadata => ({
    field: partial?.field ??
        chance.pickone(metadataFieldNames),
    value: partial?.value ??
        chance.word()
})

export const mockMetadataCollection = (n: number, partial?: Partial<Metadata>): Metadata[] =>
    Array.from({ length: n }, () => mockMetadata(partial))

export const mockSetting = (partial?: Partial<Setting>): Setting => {
    const valueAndType = (partial?.value && partial.type) ? {
        type: partial.type,
        value: partial.value
    } : chance.pickone([
        { type: 'integer', value: chance.natural({ min: 1, max: 2000 }) },
        { type: 'real', value: chance.floating({ min: 1, max: 2000 }) },
        { type: 'string', value: chance.word() },
        { type: 'boolean', value: chance.bool() },
    ])

    return {
        groupKey: partial?.groupKey ?? chance.word(),
        setting: partial?.setting ?? chance.word(),
        ...valueAndType
    } as Setting
}

export const mockSettings = (n: number, partial?: Partial<Setting>): Setting[] =>
    Array.from({ length: n }, () => mockSetting(partial))

export const mockAvatar = (partial?: Partial<Avatar>): Avatar => ({
    id: partial?.id ??
        chance.natural(),
    imageFilename: partial?.imageFilename ??
        `${chance.word()}.png`,
    imageHeight: partial?.imageHeight ??
        chance.floating({ min: 1, max: 1000 }),
    scoreBoxPositionTop: partial?.scoreBoxPositionTop ??
        chance.floating({ min: 1, max: 100 }),
    scoreBoxPositionLeft: partial?.scoreBoxPositionLeft ??
        chance.floating({ min: 1, max: 100 }),
    scoreBoxFontScale: partial?.scoreBoxFontScale ??
        chance.floating({ min: 0.1, max: 1 }),
    scoreBoxFontColor: partial?.scoreBoxFontColor ??
        chance.color()
})

export const mockAvatars = (n: number, partial?: Partial<Avatar>): Avatar[] =>
    Array.from({ length: n }, () => mockAvatar(partial))

export const mockContestant = (partial?: Partial<Contestant>): Contestant => ({
    id: partial?.id ??
        chance.guid({ version: 4 }),
    name: partial?.name ??
        chance.name(),
    avatar: partial?.avatar ??
        chance.natural()
})

export const mockContestants = (n: number, partial?: Partial<Contestant>): Contestant[] =>
    Array.from({ length: n }, () => mockContestant(partial))

export const mockSpecialEntryTopic =
    (partial?: Partial<SpecialEntryTopic>): SpecialEntryTopic => ({
        designation: partial?.designation ??
            chance.word().toUpperCase()
    })

export const mockSpecialEntryTopics =
    (n: number, partial?: Partial<SpecialEntryTopic>): SpecialEntryTopic[] =>
        Array.from({ length: n }, () => mockSpecialEntryTopic(partial))

export const mockEntry = (partial?: Partial<Entry>): Entry => ({
    id: partial?.id ??
        chance.guid({ version: 4 }),
    title: partial?.title ??
        chance.sentence({ words: 3 }),
    author: partial?.author ??
        chance.guid({ version: 4 }),
    videoUrl: partial?.videoUrl ??
        chance.url(),
    specialTopic: partial?.specialTopic ??
    chance.natural({ min: 1, max: 10 }) == 1 ? chance.word().toUpperCase() : null
})

export const mockEntries = (n: number, partial?: Partial<Entry>): Entry[] =>
    Array.from({ length: n }, () => mockEntry(partial))

export const mockScoring = (partial?: Partial<Scoring>): Scoring => ({
    contestant: partial?.contestant ??
        chance.guid({ version: 4 }),
    entry: partial?.entry ??
        chance.guid({ version: 4 }),
    score: partial?.score ??
        chance.floating({ min: 0, max: 10 })
})

export const mockScoringEntries = (n: number, partial?: Partial<Scoring>): Scoring[] =>
    Array.from({ length: n }, () => mockScoring(partial))

export const mockTemplate = (partial?: Partial<Template>): Template => ({
    entry: partial?.entry ??
        chance.guid({ version: 4 }),
    avatarScale: partial?.avatarScale ??
        chance.floating({ min: 0.1, max: 1 }),
    authorAvatarScale: partial?.authorAvatarScale ??
        chance.floating({ min: 0.1, max: 1 }),
    videoBoxWidthPx: partial?.videoBoxWidthPx ??
        chance.natural({ min: 1, max: 1280 }),
    videoBoxHeightPx: partial?.videoBoxHeightPx ??
        chance.natural({ min: 1, max: 720 }),
    videoBoxPositionTopPx: partial?.videoBoxPositionTopPx ??
        chance.natural({ min: 1, max: 1000 }),
    videoBoxPositionLeftPx: partial?.videoBoxPositionLeftPx ??
        chance.natural({ min: 1, max: 1000 }),
})

export const mockTemplates = (n: number, partial?: Partial<Template>): Template[] =>
    Array.from({ length: n }, () => mockTemplate(partial))

export const mockVideoOption = (partial?: Partial<VideoOptions>): VideoOptions => ({
    entry: partial?.entry ??
        chance.guid({ version: 4 }),
    timestampStart: partial?.timestampStart ??
        `${chance.pad(
            chance.natural({ min: 0, max: 59 }), 2)}:${chance.pad(chance.natural({ min: 0, max: 59 }),
            2)}`,
    timestampEnd: partial?.timestampEnd ??
        `${chance.pad(
            chance.natural({ min: 0, max: 59 }), 2)}:${chance.pad(chance.natural({ min: 0, max: 59 }),
            2)}`,
})

export const mockVideoOptionsCollection =
    (n: number, partial?: Partial<VideoOptions>): VideoOptions[] =>
        Array.from({ length: n }, () => mockVideoOption(partial))

export const mockContestantStats =
    (partial?: Partial<ContestantStats>): ContestantStats => ({
        contestant: partial?.contestant ??
            chance.guid({ version: 4 }),
        avgGivenScore: partial?.avgGivenScore ??
            chance.floating({ min: 0, max: 10 }),
        avgReceivedScore: partial?.avgReceivedScore ??
            chance.floating({ min: 0, max: 10 })
    })

export const mockContestantsStats =
    (n: number, partial?: Partial<ContestantStats>): ContestantStats[] =>
        Array.from({ length: n }, () => mockContestantStats(partial))

export const mockEntryStats = (partial?: Partial<EntryStats>): EntryStats => ({
    entry: partial?.entry ??
        chance.guid({ version: 4 }),
    avgScore: partial?.avgScore ??
        chance.floating({ min: 0, max: 10 }),
    rankingPlace: partial?.rankingPlace ??
        chance.natural({ min: 1, max: 100 }),
    rankingSequence: partial?.rankingSequence ??
        chance.natural({ min: 1, max: 100 })
})

export const mockEntriesStats = (n: number, partial?: Partial<EntryStats>): EntryStats[] =>
    Array.from({ length: n }, () => mockEntryStats(partial))