import { Chance } from 'chance'

import {
    Avatar,
    Award,
    CastVote,
    Member,
    Metadata,
    MetadataFields,
    Nomination,
    NominationStats,
    Setting,
    Template,
    VideoOptions,
    Videoclip,
} from '@/db/models'

const chance = new Chance()

const metadataFieldNames: MetadataFields[] = ['edition', 'topic', 'organiser', 'start_date']
export const mockMetadata = (partial?: Partial<Metadata>): Metadata => ({
    field: partial?.field ?? chance.pickone(metadataFieldNames),
    value: partial?.value ?? chance.word(),
})

export const mockMetadataCollection = (n: number, partial?: Partial<Metadata>): Metadata[] =>
    Array.from({ length: n }, () => mockMetadata(partial))

export const mockSetting = (partial?: Partial<Setting>): Setting => {
    const valueAndType =
        partial?.value && partial.type
            ? {
                  type: partial.type,
                  value: partial.value,
              }
            : chance.pickone([
                  { type: 'integer', value: chance.natural({ min: 1, max: 2000 }) },
                  { type: 'real', value: chance.floating({ min: 1, max: 2000 }) },
                  { type: 'string', value: chance.word() },
                  { type: 'boolean', value: chance.bool() },
              ])

    return {
        groupKey: partial?.groupKey ?? chance.word(),
        setting: partial?.setting ?? chance.word(),
        ...valueAndType,
    } as Setting
}

export const mockSettings = (n: number, partial?: Partial<Setting>): Setting[] =>
    Array.from({ length: n }, () => mockSetting(partial))

export const mockAvatar = (partial?: Partial<Avatar>): Avatar => ({
    id: partial?.id ?? chance.natural(),
    imageFilename: partial?.imageFilename ?? `${chance.word()}.png`,
    imageHeight: partial?.imageHeight ?? chance.floating({ min: 1, max: 1000 }),
    scoreBoxPositionTop: partial?.scoreBoxPositionTop ?? chance.floating({ min: 1, max: 100 }),
    scoreBoxPositionLeft: partial?.scoreBoxPositionLeft ?? chance.floating({ min: 1, max: 100 }),
    scoreBoxFontScale: partial?.scoreBoxFontScale ?? chance.floating({ min: 0.1, max: 1 }),
    scoreBoxFontColor: partial?.scoreBoxFontColor ?? chance.color(),
})

export const mockAvatars = (n: number, partial?: Partial<Avatar>): Avatar[] =>
    Array.from({ length: n }, () => mockAvatar(partial))

export const mockMember = (partial?: Partial<Member>): Member => ({
    id: partial?.id ?? chance.guid({ version: 4 }),
    name: partial?.name ?? chance.name(),
    avatar: partial?.avatar ?? chance.natural(),
})

export const mockMembers = (n: number, partial?: Partial<Member>): Member[] =>
    Array.from({ length: n }, () => mockMember(partial))

export const mockAward = (partial?: Partial<Award>): Award => ({
    slug: partial?.slug ?? chance.n<string>(() => chance.word(), 3).join('-'),
    designation: partial?.designation ?? chance.sentence({ words: 5 }),
})

export const mockAwards = (n: number, partial?: Partial<Award>): Award[] =>
    Array.from({ length: n }, () => mockAward(partial))

export const mockNomination = (partial?: Partial<Nomination>): Nomination => ({
    id: partial?.id ?? chance.guid({ version: 4 }),
    gameTitle: partial?.gameTitle ?? chance.sentence({ words: 3 }),
    nominee: partial?.nominee ?? chance.sentence({ words: 2 }),
    award: partial?.award ?? chance.n<string>(() => chance.word(), 3).join('-'),
})

export const mockNominations = (n: number, partial?: Partial<Nomination>): Nomination[] =>
    Array.from({ length: n }, () => mockNomination(partial))

export const mockTemplate = (partial?: Partial<Template>): Template => ({
    nomination: partial?.nomination ?? chance.guid({ version: 4 }),
    avatarScale: partial?.avatarScale ?? chance.floating({ min: 0.1, max: 1 }),
    videoBoxWidthPx: partial?.videoBoxWidthPx ?? chance.natural({ min: 1, max: 1280 }),
    videoBoxHeightPx: partial?.videoBoxHeightPx ?? chance.natural({ min: 1, max: 720 }),
    videoBoxPositionTopPx: partial?.videoBoxPositionTopPx ?? chance.natural({ min: 1, max: 1000 }),
    videoBoxPositionLeftPx: partial?.videoBoxPositionLeftPx ?? chance.natural({ min: 1, max: 1000 }),
})

export const mockTemplates = (n: number, partial?: Partial<Template>): Template[] =>
    Array.from({ length: n }, () => mockTemplate(partial))

export const mockVideoclip = (partial?: Partial<Videoclip>): Videoclip => ({
    id: partial?.id ?? chance.natural(),
    url: partial?.url ?? chance.url(),
})

export const mockVideoclips = (n: number, partial?: Partial<Videoclip>): Videoclip[] =>
    Array.from({ length: n }, () => mockVideoclip(partial))

export const mockVideoOptions = (partial?: Partial<VideoOptions>): VideoOptions => ({
    nomination: partial?.nomination ?? chance.guid({ version: 4 }),
    videoclip: partial?.videoclip ?? chance.natural(),
    timestampStart:
        partial?.timestampStart ??
        `${chance.pad(chance.natural({ min: 0, max: 59 }), 2)}:${chance.pad(chance.natural({ min: 0, max: 59 }), 2)}`,
    timestampEnd:
        partial?.timestampEnd ??
        `${chance.pad(chance.natural({ min: 0, max: 59 }), 2)}:${chance.pad(chance.natural({ min: 0, max: 59 }), 2)}`,
})

export const mockVideoOptionsCollection = (n: number, partial?: Partial<VideoOptions>): VideoOptions[] =>
    Array.from({ length: n }, () => mockVideoOptions(partial))

export const mockCastVote = (partial?: Partial<CastVote>): CastVote => ({
    member: partial?.member ?? chance.guid({ version: 4 }),
    nomination: partial?.nomination ?? chance.guid({ version: 4 }),
    score: partial?.score ?? chance.floating({ min: 0, max: 10 }),
})

export const mockScoringEntries = (n: number, partial?: Partial<CastVote>): CastVote[] =>
    Array.from({ length: n }, () => mockCastVote(partial))

export const mockNominationStats = (partial?: Partial<NominationStats>): NominationStats => ({
    nomination: partial?.nomination ?? chance.guid({ version: 4 }),
    avgScore: partial?.avgScore ?? chance.floating({ min: 0, max: 10 }),
    rankingPlace: partial?.rankingPlace ?? chance.natural({ min: 1, max: 100 }),
    rankingSequence: partial?.rankingSequence ?? chance.natural({ min: 1, max: 100 }),
})

export const mockNominationsStats = (n: number, partial?: Partial<NominationStats>): NominationStats[] =>
    Array.from({ length: n }, () => mockNominationStats(partial))