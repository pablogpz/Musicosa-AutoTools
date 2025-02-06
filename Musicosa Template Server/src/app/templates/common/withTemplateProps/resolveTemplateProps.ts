import fs from 'fs'
import path from 'path'
import { eq } from 'drizzle-orm'

import formatNumberToDecimalPrecision from '@/formatters/formatNumberToDecimalPrecision'

import db from '@/db/database'
import {
    Avatar,
    Award,
    awards,
    CastVote,
    castVotes,
    Member,
    Nomination,
    nominations,
    nominationStats,
    NominationStats,
    Template,
    templates,
    TypedSetting
} from '@/db/schema'
import { defaultAvatar, defaultCastVote } from '@/db/defaults'
import membersRepository from '@/db/repository/members'
import avatarsRepository from '@/db/repository/avatars'
import settingsRepository from '@/db/repository/settings'
import { DEFAULT_DISPLAY_DECIMAL_DIGITS } from '@/app/defaults'

export type ResolvedNominationStats = NominationStats & { formattedAvgScore: string }

export type ResolvedAvatar = Omit<Avatar, 'imageFilename'> & { resolvedImageFilename: string }

export type ResolvedCastVote = CastVote & { formattedScore: string }

export type ResolvedMember = Omit<Member, 'avatar'> & { avatar: ResolvedAvatar, vote: ResolvedCastVote }

export type ResolvedTemplateProps =
    Pick<Nomination, 'gameTitle' | 'nominee'> &
    Pick<ResolvedNominationStats, 'rankingPlace' | 'formattedAvgScore'> &
    Pick<Template, 'avatarScale' | 'videoBoxWidthPx' | 'videoBoxHeightPx'> &
    {
        award: Award
        members: ResolvedMember[]
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

function resolveCastVote(vote: CastVote, displayDecimalDigits: number): ResolvedCastVote {
    const { score } = vote

    return {
        ...vote,
        formattedScore: formatNumberToDecimalPrecision(score, displayDecimalDigits)
    } satisfies ResolvedCastVote
}

function resolveMember(baseMember: Member, avatar: Avatar, vote: CastVote, displayDecimalDigits: number): ResolvedMember {
    return {
        ...baseMember,
        avatar: resolveAvatar(avatar),
        vote: resolveCastVote(vote, displayDecimalDigits)
    } satisfies ResolvedMember
}

export const resolveTemplateProps = async (templateUUID: string): Promise<ResolvedTemplateProps | undefined> => {
    const templateResult = await db
        .select({
            avatarScale: templates.avatarScale,
            videoBoxWidthPx: templates.videoBoxWidthPx,
            videoBoxHeightPx: templates.videoBoxHeightPx
        })
        .from(templates)
        .where(eq(templates.nomination, templateUUID))

    if (templateResult.length === 0) return undefined

    // Data independent from template uuid

    const allMembers = await membersRepository.getMembers()
    const avatars = await avatarsRepository.getAvatars()

    // Data dependent on template uuid

    const template = templateResult[0]
    const nomination = await (db
        .select({
            gameTitle: nominations.gameTitle,
            nominee: nominations.nominee,
            award: nominations.award
        })
        .from(nominations)
        .where(eq(nominations.id, templateUUID)))
        .then(results => results[0])
    const award = await db
        .select()
        .from(awards)
        .where(eq(awards.slug, nomination.award))
        .then(results => results[0])
    const stats = await (db
        .select({
            rankingPlace: nominationStats.rankingPlace,
            avgScore: nominationStats.avgScore
        })
        .from(nominationStats)
        .where(eq(nominationStats.nomination, templateUUID)))
        .then(results => results[0])
    const votes = await db
        .select()
        .from(castVotes)
        .where(eq(castVotes.nomination, templateUUID))

    const displayDecimalDigitsSetting: TypedSetting<number> | undefined =
        await settingsRepository.getSettingByKey('templates.display_decimal_digits')
    const displayDecimalDigits = displayDecimalDigitsSetting?.value ?? DEFAULT_DISPLAY_DECIMAL_DIGITS

    const members = allMembers
        .map(m => resolveMember(m,
            avatars.find(avatar => avatar.id === m.avatar) ?? defaultAvatar,
            votes.find(vote => vote.member === m.id) ?? defaultCastVote,
            displayDecimalDigits))

    return {
        gameTitle: nomination.gameTitle,
        nominee: nomination.nominee,
        rankingPlace: stats.rankingPlace,
        formattedAvgScore: formatNumberToDecimalPrecision(stats.avgScore!, displayDecimalDigits),
        avatarScale: template.avatarScale,
        videoBoxWidthPx: template.videoBoxWidthPx,
        videoBoxHeightPx: template.videoBoxHeightPx,
        award,
        members: members
    }
}