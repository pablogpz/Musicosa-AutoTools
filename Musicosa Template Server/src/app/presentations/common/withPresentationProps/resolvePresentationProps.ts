import { eq } from 'drizzle-orm'

import db from '@/db/database'
import { defaultNominationStats } from '@/db/defaults'
import entriesRepository from '@/db/repositories/nominations'
import { nominationStats } from '@/db/schema'

export type ResolvedPresentationProps = {
    rankingPlace: number
    sequenceNumberInTie: [number, number] | undefined
}

export async function resolvePresentationProps(nominationId: string): Promise<ResolvedPresentationProps | undefined> {
    const nominationStatsResult = await db
        .select({
            rankingPlace: nominationStats.rankingPlace,
        })
        .from(nominationStats)
        .where(eq(nominationStats.nomination, nominationId))

    if (nominationStatsResult.length === 0) return undefined

    const stats = nominationStatsResult[0]

    const sequenceNumberInTie = await entriesRepository.getSequenceNumberInTie(nominationId)

    return {
        rankingPlace: stats.rankingPlace ?? defaultNominationStats.rankingPlace!,
        sequenceNumberInTie,
    }
}
