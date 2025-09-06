import { defaultAvatar, defaultCastVote, defaultMember } from '@/db/defaults'

import { ResolvedAvatar, ResolvedCastVote, ResolvedMember } from './resolveTemplateProps'
import { TemplateSettingsProps } from './withTemplateProps'

export const defaultTemplateSettingsProps: TemplateSettingsProps = {
    scoreMinValue: 0,
    scoreMaxValue: 10,
}

export const defaultResolvedAvatar: ResolvedAvatar = {
    ...defaultAvatar,
    resolvedImageFilename: defaultAvatar.imageFilename,
}

export const defaultResolvedCastVote: ResolvedCastVote = {
    ...defaultCastVote,
    formattedScore: defaultCastVote.score.toString(),
}

export const defaultResolvedMember: ResolvedMember = {
    ...defaultMember,
    avatar: defaultResolvedAvatar,
    vote: defaultResolvedCastVote,
}
