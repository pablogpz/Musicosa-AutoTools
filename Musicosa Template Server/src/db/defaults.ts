import { Avatar, Contestant, Entry, EntryStats, Scoring, Template } from '@/db/schema'

export const defaultAvatarId = 0

export const defaultAvatar: Avatar = {
    id: defaultAvatarId,
    imageFilename: 'unknown.png',
    imageHeight: 584.0,
    scoreBoxPositionTop: 25.0,
    scoreBoxPositionLeft: 73.5,
    scoreBoxFontScale: 0.1,
    scoreBoxFontColor: 'black'
}

export const defaultContestantId = '00000000-0000-0000-0000-000000000000'

export const defaultContestant: Contestant = {
    id: defaultContestantId,
    name: 'Participante',
    avatar: defaultAvatarId,
}

export const defaultAuthor: Contestant = {
    id: defaultContestantId,
    name: 'Tipo de Incógnito',
    avatar: defaultAvatarId,
}

export const defaultEntryId = "00000000-0000-0000-0000-100000000000"

export const defaultEntry: Entry = {
    id: defaultEntryId,
    author: defaultAuthor.id,
    title: 'Título de la entrada',
    videoUrl: 'https://www.youtube.com/watch?v=CVyPO_tR540',
    specialTopic: 'INFANCIA'
}

export const defaultScoring: Scoring = {
    contestant: defaultContestantId,
    entry: defaultEntryId,
    score: 9.99,
}

export const defaultEntryStats: EntryStats = {
    entry: defaultEntryId,
    avgScore: 9.99,
    rankingPlace: 1,
    rankingSequence: 1,
}

export const defaultTemplate: Template = {
    entry: defaultEntryId,
    avatarScale: 0.5,
    videoBoxWidthPx: 1280,
    videoBoxHeightPx: 720,
    videoBoxPositionTopPx: 86,
    videoBoxPositionLeftPx: 720,
}