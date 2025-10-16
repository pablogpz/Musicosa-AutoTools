import { Avatar, Contestant, Entry, EntryStats, Scoring, Template } from '@/db/models'

export const defaultAvatarId = 0

export const defaultAvatar: Avatar = {
    id: defaultAvatarId,
    imageFilename: 'unknown.png',
    imageHeight: 397.0,
    scoreBoxPositionTop: 17.5,
    scoreBoxPositionLeft: 81,
    scoreBoxFontScale: 0.175,
    scoreBoxFontColor: 'black',
}

export const defaultContestantId = '00000000-0000-0000-0000-000000000000'

export const defaultContestant: Contestant = {
    id: defaultContestantId,
    name: 'Participante',
    avatar: defaultAvatarId,
}

export const defaultAuthor: Contestant = {
    id: defaultContestantId,
    name: 'Autor',
    avatar: defaultAvatarId,
}

export const defaultEntryId = '00000000-0000-0000-0000-100000000000'

export const defaultEntry: Entry = {
    id: defaultEntryId,
    author: defaultAuthor.id,
    title: 'Título de la entrada - Obra',
    videoUrl: 'https://www.youtube.com/watch?v=CVyPO_tR540',
    topic: '',
}

export const defaultScoring: Scoring = {
    contestant: defaultContestantId,
    entry: defaultEntryId,
    score: 9.99,
    estrelli: 0,
}

export const defaultEntryStats: EntryStats = {
    entry: defaultEntryId,
    avgScore: 9.99,
    rankingPlace: 70,
    rankingSequence: 70,
}

export const defaultTemplate: Template = {
    entry: defaultEntryId,
    avatarScale: 0.35,
    authorAvatarScale: 0,
    videoBoxWidthPx: 1150,
    videoBoxHeightPx: 648,
    videoBoxPositionTopPx: 45,
    videoBoxPositionLeftPx: 702,
}
