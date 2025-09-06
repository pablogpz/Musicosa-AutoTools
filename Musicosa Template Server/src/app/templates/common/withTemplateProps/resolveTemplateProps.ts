import fs from 'fs'
import path from 'path'
import { eq } from 'drizzle-orm'

import formatNumberToDecimalPrecision from '@/formatters/formatNumberToDecimalPrecision'

import db from '@/db/database'
import { entries, entriesStats, scoring, templates } from '@/db/schema'
import { defaultAuthor, defaultAvatar, defaultScoring } from '@/db/defaults'
import contestantsRepository from '@/db/repositories/contestants'
import avatarsRepository from '@/db/repositories/avatars'
import settingsRepository from '@/db/repositories/settings'
import entriesRepository from '@/db/repositories/entries'
import { DEFAULT_DISPLAY_DECIMAL_DIGITS } from '@/app/defaults'
import { Avatar, Contestant, Entry, EntryStats, Scoring, Template } from '@/db/models'

export type ResolvedEntryStats = EntryStats & { formattedAvgScore: string }

export type ResolvedAvatar = Omit<Avatar, 'imageFilename'> & { resolvedImageFilename: string }

export type ResolvedScoring = Omit<Scoring, 'contestant' | 'entry'> & { formattedScore: string }

export type ResolvedContestant = Omit<Contestant, 'avatar'> & { avatar: ResolvedAvatar, scoring: ResolvedScoring }

export type ResolvedTemplateProps =
    Pick<Template, 'avatarScale' | 'authorAvatarScale' | 'videoBoxWidthPx' | 'videoBoxHeightPx'> &
    Pick<Entry, 'title' | 'specialTopic'> &
    Pick<ResolvedEntryStats, 'rankingPlace' | 'formattedAvgScore'> &
    {
        avgScoreDelta: number,
        author: ResolvedContestant,
        sequenceNumberInAuthorEntries: [number, number],
        sequenceNumberInSpecialTopic: [number, number] | undefined,
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

export async function resolveTemplateProps(templateId: string): Promise<ResolvedTemplateProps | undefined> {
    const templateResult = await db
        .select({
            avatarScale: templates.avatarScale,
            authorAvatarScale: templates.authorAvatarScale,
            videoBoxWidthPx: templates.videoBoxWidthPx,
            videoBoxHeightPx: templates.videoBoxHeightPx
        })
        .from(templates)
        .where(eq(templates.entry, templateId))
    if (templateResult.length === 0) return undefined

    // Data independent from template id

    const displayDecimalDigitsSetting =
        await settingsRepository.getSettingByKey<number>('templates.display_decimal_digits')
    const displayDecimalDigits = displayDecimalDigitsSetting?.value ?? DEFAULT_DISPLAY_DECIMAL_DIGITS

    const allContestants = await contestantsRepository.getContestants()
    const avatars = await avatarsRepository.getAvatars()

    // Data dependent on template id

    const template = templateResult[0]
    const entry = await (db
        .select({
            title: entries.title,
            author: entries.author,
            specialTopic: entries.specialTopic
        })
        .from(entries)
        .where(eq(entries.id, templateId)))
        .then(results => results[0])
    const entryStats = await (db
        .select({
            rankingPlace: entriesStats.rankingPlace,
            avgScore: entriesStats.avgScore
        })
        .from(entriesStats)
        .where(eq(entriesStats.entry, templateId)))
        .then(results => results[0])
    const scoringEntries = await db.select().from(scoring).where(eq(scoring.entry, templateId))

    const avgScoreDelta = await entriesRepository.getAvgScoreDeltaFromPreviousEntry(templateId)
    if (avgScoreDelta === undefined) return undefined

    const author =
        allContestants.find(contestant => contestant.id === entry.author) ?? defaultAuthor
    const authorAvatar =
        avatars.find(avatar => avatar.id === author.avatar) ?? defaultAvatar
    const authorScoring =
        scoringEntries.find(scoring => scoring.contestant === author.id) ?? defaultScoring

    const sequenceNumberInAuthorEntries =
        await entriesRepository.getSequenceNumberInAuthorEntries(templateId)
    if (!sequenceNumberInAuthorEntries) return undefined

    const sequenceNumberInSpecialTopic =
        await entriesRepository.getSequenceNumberInSpecialTopic(templateId)

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
        avgScoreDelta,
        avatarScale: template.avatarScale,
        authorAvatarScale: template.authorAvatarScale,
        videoBoxWidthPx: template.videoBoxWidthPx,
        videoBoxHeightPx: template.videoBoxHeightPx,
        author: resolveContestant(author, authorAvatar, authorScoring, displayDecimalDigits),
        sequenceNumberInAuthorEntries,
        sequenceNumberInSpecialTopic,
        contestants: contestants
    }
}