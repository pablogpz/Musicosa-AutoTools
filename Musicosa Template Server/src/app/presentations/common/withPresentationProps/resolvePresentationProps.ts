import { eq } from 'drizzle-orm'

import db from '@/db/database'
import { entriesStats } from '@/db/schema'

export type ResolvedPresentationProps = {
    rankingPlace: number
}

const DEFAULT_RANKING_PLACE = 0

export const resolvePresentationProps = async (entryUUID: string): Promise<ResolvedPresentationProps | undefined> => {
    const entryStatsResult = await db
        .select({
            rankingPlace: entriesStats.rankingPlace
        })
        .from(entriesStats)
        .where(eq(entriesStats.entry, entryUUID))

    if (entryStatsResult.length === 0) return undefined

    const entryStats = entryStatsResult[0]

    return {
        rankingPlace: entryStats.rankingPlace ?? DEFAULT_RANKING_PLACE
    }
}