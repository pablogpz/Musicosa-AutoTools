import fs from 'fs'
import path from 'path'
import { eq } from 'drizzle-orm'

import formatNumberToDecimalPrecision from '@/formatters/formatNumberToDecimalPrecision'

import db from '@/db/database'
import {
    Avatar,
    Contestant,
    entries,
    entriesStats,
    Entry,
    EntryStats,
    Scoring,
    scoring,
    Template,
    templates,
    TypedSetting
} from '@/db/schema'
import { defaultAuthor, defaultAvatar, defaultScoring } from '@/db/defaults'
import contestantsRepository from '@/db/repository/contestants'
import avatarsRepository from '@/db/repository/avatars'
import settingsRepository from '@/db/repository/settings'
import { DEFAULT_DISPLAY_DECIMAL_DIGITS } from '@/app/defaults'

export type ResolvedEntryStats = EntryStats & { formattedAvgScore: string }

export type ResolvedAvatar = Omit<Avatar, 'imageFilename'> & { resolvedImageFilename: string }

export type ResolvedScoring = Scoring & { formattedScore: string }

export type ResolvedContestant = Omit<Contestant, 'avatar'> & { avatar: ResolvedAvatar, scoring: ResolvedScoring }

export type ResolvedTemplateProps =
    Pick<Template, 'avatarScale' | 'authorAvatarScale' | 'videoBoxWidthPx' | 'videoBoxHeightPx'> &
    Pick<Entry, 'title' | 'specialTopic'> &
    Pick<ResolvedEntryStats, 'rankingPlace' | 'formattedAvgScore'> &
    {
        author: ResolvedContestant
        contestants: ResolvedContestant[]
    }

function resolveAvatar(avatar: Avatar): ResolvedAvatar {
    const { imageFilename } = avatar
    let imageWithFallback

    if (fs.existsSync(path.join(process.cwd(), 'public/avatars/', imageFilename)))
        imageWithFallback = imageFilename
    else
        imageWithFallback = defaultAvatar.imageFilename

    return {
        ...avatar,
        resolvedImageFilename: imageWithFallback
    } satisfies ResolvedAvatar
}

function resolveScoring(scoring: Scoring, displayDecimalDigits: number): ResolvedScoring {
    const { score } = scoring

    return {
        ...scoring,
        formattedScore: formatNumberToDecimalPrecision(score, displayDecimalDigits)
    } satisfies ResolvedScoring
}

function resolveContestant(baseContestant: Contestant, avatar: Avatar, scoring: Scoring,
                           displayDecimalDigits: number): ResolvedContestant {
    return {
        ...baseContestant,
        avatar: resolveAvatar(avatar),
        scoring: resolveScoring(scoring, displayDecimalDigits)
    } satisfies ResolvedContestant
}

export const resolveTemplateProps = async (templateUUID: string): Promise<ResolvedTemplateProps | undefined> => {
    const templateResult = await db
        .select({
            avatarScale: templates.avatarScale,
            authorAvatarScale: templates.authorAvatarScale,
            videoBoxWidthPx: templates.videoBoxWidthPx,
            videoBoxHeightPx: templates.videoBoxHeightPx
        })
        .from(templates)
        .where(eq(templates.entry, templateUUID))

    if (templateResult.length === 0) return undefined

    // Data independent from template uuid

    const allContestants = await contestantsRepository.getContestants()
    const avatars = await avatarsRepository.getAvatars()

    // Data dependent on template uuid

    const template = templateResult[0]
    const entry = await (db
        .select({
            title: entries.title,
            author: entries.author,
            specialTopic: entries.specialTopic
        })
        .from(entries)
        .where(eq(entries.id, templateUUID)))
        .then(results => results[0])
    const entryStats = await (db
        .select({
            rankingPlace: entriesStats.rankingPlace,
            avgScore: entriesStats.avgScore
        })
        .from(entriesStats)
        .where(eq(entriesStats.entry, templateUUID)))
        .then(results => results[0])
    const scoringEntries = await db.select().from(scoring).where(eq(scoring.entry, templateUUID))

    const displayDecimalDigitsSetting: TypedSetting<number> | undefined =
        await settingsRepository.getSettingByKey('templates.display_decimal_digits')
    const displayDecimalDigits = displayDecimalDigitsSetting?.value ?? DEFAULT_DISPLAY_DECIMAL_DIGITS

    const author =
        allContestants.find(contestant => contestant.id === entry.author) ?? defaultAuthor
    const authorAvatar =
        avatars.find(avatar => avatar.id === author.avatar) ?? defaultAvatar
    const authorScoring =
        scoringEntries.find(scoring => scoring.contestant === author.id) ?? defaultScoring

    const contestants = allContestants
        .filter(contestant => contestant.id !== entry.author)
        .map(c => resolveContestant(
            c,
            avatars.find(avatar => avatar.id === c.avatar) ?? defaultAvatar,
            scoringEntries.find(scoring => scoring.contestant === c.id) ?? defaultScoring,
            displayDecimalDigits))

    return {
        title: entry.title,
        specialTopic: entry.specialTopic,
        rankingPlace: entryStats.rankingPlace,
        formattedAvgScore: formatNumberToDecimalPrecision(entryStats.avgScore!, displayDecimalDigits),
        avatarScale: template.avatarScale,
        authorAvatarScale: template.authorAvatarScale,
        videoBoxWidthPx: template.videoBoxWidthPx,
        videoBoxHeightPx: template.videoBoxHeightPx,
        author: resolveContestant(author, authorAvatar, authorScoring, displayDecimalDigits),
        contestants: contestants
    }
}