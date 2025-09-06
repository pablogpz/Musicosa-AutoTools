import { defaultAuthor, defaultAvatar, defaultContestant, defaultScoring } from '@/db/defaults'

import { ResolvedAvatar, ResolvedContestant, ResolvedScoring, ResolvedTemplateProps } from './resolveTemplateProps'
import { TemplateSettingsProps } from './withTemplateProps'

export const defaultTemplateSettingsProps: TemplateSettingsProps = {
    scoreMinValue: 0,
    scoreMaxValue: 10,
}

export const defaultResolvedAvatar: ResolvedAvatar = {
    ...defaultAvatar,
    resolvedImageFilename: defaultAvatar.imageFilename,
}

export const defaultResolvedScoring: ResolvedScoring = {
    ...defaultScoring,
    formattedScore: defaultScoring.score.toString(),
}

export const defaultResolvedAuthor: ResolvedContestant = {
    ...defaultAuthor,
    avatar: defaultResolvedAvatar,
    scoring: defaultResolvedScoring,
}

export const defaultResolvedContestant: ResolvedContestant = {
    ...defaultContestant,
    avatar: defaultResolvedAvatar,
    scoring: defaultResolvedScoring,
}

export const defaultSequenceNumberInAuthorEntries: ResolvedTemplateProps['sequenceNumberInAuthorEntries'] = [1, 2]

export const defaultSequenceNumberInSpecialTopic: ResolvedTemplateProps['sequenceNumberInSpecialTopic'] = [1, 2]

export const defaultAvgScoreDelta: ResolvedTemplateProps['avgScoreDelta'] = 0.5
