import { eq } from 'drizzle-orm'

import db from '@/db/database'
import { defaultNominationStats } from '@/db/defaults'
import { nominationStats } from '@/db/schema'

export type ResolvedPresentationProps = {
    rankingPlace: number
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

    return {
        rankingPlace: stats.rankingPlace ?? defaultNominationStats.rankingPlace!,
    }
}
