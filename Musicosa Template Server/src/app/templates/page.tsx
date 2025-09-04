import { notFound } from 'next/navigation'
import { and, eq } from 'drizzle-orm'

import db from '@/db/database'
import { nominations, nominationStats } from '@/db/schema'
import templateFactory from '@/app/templates/components/Template/templateFactory'
import FrameContainer from '@/app/components/FrameContainer'

export default async function Page({ searchParams }: {
    searchParams: Promise<{ [key: string]: string | string[] | undefined }>
}) {
    const { award, q } = await searchParams

    if (!award || typeof award !== "string")
        notFound()
    if (!q || typeof q !== "string" || isNaN(Number(q)))
        notFound()

    const requestedSequenceNumber = parseInt(q)

    const nominationsIdSubquery = db
        .select({ nominationId: nominations.id })
        .from(nominations)
        .innerJoin(nominationStats, eq(nominationStats.nomination, nominations.id))
        .where(and(eq(nominations.award, award), eq(nominationStats.rankingSequence, requestedSequenceNumber)))
        .as("sq")
    const template = await db
        .select({ nominationId: nominations.id })
        .from(nominations)
        .innerJoin(nominationsIdSubquery, eq(nominations.id, nominationsIdSubquery.nominationId))

    if (!template.length)
        notFound()

    const TemplateComponent = await templateFactory(template[0].nominationId)

    return TemplateComponent && (
        <FrameContainer>
            <TemplateComponent/>
        </FrameContainer>
    )
}

