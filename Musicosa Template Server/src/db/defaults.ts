import { Avatar, Award, Member, Nomination, NominationStats, CastVote, Template } from '@/db/schema'

export const defaultAvatarId = 0

export const defaultAvatar: Avatar = {
    id: defaultAvatarId,
    imageFilename: 'unknown.png',
    imageHeight: 397.0,
    scoreBoxPositionTop: 17.5,
    scoreBoxPositionLeft: 81,
    scoreBoxFontScale: 0.175,
    scoreBoxFontColor: 'black'
}

export const defaultMemberId = '00000000-0000-0000-0000-000000000000'

export const defaultMember: Member = {
    id: defaultMemberId,
    name: 'Miembro',
    avatar: defaultAvatarId,
}

export const defaultAwardSlug = 'el-killer-no-tu-abuela'
export const defaultAwardDesignation = 'El Killer, no tu Abuela'

export const defaultAward: Award = {
    slug: defaultAwardSlug,
    designation: defaultAwardDesignation
}

export const defaultNominationId = '00000000-0000-0000-0000-100000000000'

export const defaultNomination: Nomination = {
    id: defaultNominationId,
    gameTitle: 'Título del juego',
    nominee: 'Nominado',
    award: defaultAwardSlug
}

export const defaultTemplate: Template = {
    nomination: defaultNominationId,
    avatarScale: 0.45,
    videoBoxWidthPx: 1200,
    videoBoxHeightPx: 676,
    videoBoxPositionTopPx: 59,
    videoBoxPositionLeftPx: 658
}

export const defaultCastVote: CastVote = {
    member: defaultMemberId,
    nomination: defaultNominationId,
    score: 9.99,
}

export const defaultNominationStats: NominationStats = {
    nomination: defaultNominationId,
    avgScore: 9.99,
    rankingPlace: 5,
    rankingSequence: 5,
}
