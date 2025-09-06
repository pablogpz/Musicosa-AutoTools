import { eq } from 'drizzle-orm'

import db from '@/db/database'
import { defaultEntryStats } from '@/db/defaults'
import { entriesStats } from '@/db/schema'

export type ResolvedPresentationProps = {
    rankingPlace: number
}

export async function resolvePresentationProps(entryId: string): Promise<ResolvedPresentationProps | undefined> {
    const entryStatsResult = await db
        .select({
            rankingPlace: entriesStats.rankingPlace,
        })
        .from(entriesStats)
        .where(eq(entriesStats.entry, entryId))

    if (entryStatsResult.length === 0) return undefined

    return {
        rankingPlace: entryStatsResult[0].rankingPlace ?? defaultEntryStats.rankingPlace!,
    }
}
