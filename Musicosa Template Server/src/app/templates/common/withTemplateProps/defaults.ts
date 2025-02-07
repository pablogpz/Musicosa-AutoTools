import { defaultAuthor, defaultAvatar, defaultContestant, defaultScoring } from '@/db/defaults'

import { ResolvedAvatar, ResolvedContestant, ResolvedScoring } from './resolveTemplateProps'

export const defaultResolvedAvatar: ResolvedAvatar = {
    ...defaultAvatar,
    resolvedImageFilename: defaultAvatar.imageFilename
}

export const defaultResolvedScoring: ResolvedScoring = {
    ...defaultScoring,
    formattedScore: defaultScoring.score.toString()
}

export const defaultResolvedAuthor: ResolvedContestant = {
    ...defaultAuthor,
    avatar: defaultResolvedAvatar,
    scoring: defaultResolvedScoring
}

export const defaultResolvedContestant: ResolvedContestant = {
    ...defaultContestant,
    avatar: defaultResolvedAvatar,
    scoring: defaultResolvedScoring
}
