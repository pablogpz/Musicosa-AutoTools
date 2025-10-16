import { and, eq } from 'drizzle-orm'
import { notFound } from 'next/navigation'

import FrameContainer from '@/app/components/FrameContainer'
import { templateFactory } from '@/app/templates/components/Template'
import db from '@/db/database'
import { nominationStats, nominations } from '@/db/schema'

type SearchParams = { award: string, q: string }

export default async function Page({ searchParams }: { searchParams: Promise<SearchParams> }) {
    const { award, q } = await searchParams

    if (!award) notFound()
    if (!q || isNaN(Number(q))) notFound()

    const requestedSequenceNumber = parseInt(q)

    const nominationsIdSubquery = db
        .select({ nominationId: nominations.id })
        .from(nominations)
        .innerJoin(nominationStats, eq(nominationStats.nomination, nominations.id))
        .where(and(eq(nominations.award, award), eq(nominationStats.rankingSequence, requestedSequenceNumber)))
        .as('sq')
    const template = await db
        .select({ nominationId: nominations.id })
        .from(nominations)
        .innerJoin(nominationsIdSubquery, eq(nominations.id, nominationsIdSubquery.nominationId))

    if (template.length == 0) notFound()

    const TemplateComponent = await templateFactory(template[0].nominationId)

    return (
        TemplateComponent && (
            <FrameContainer>
                <TemplateComponent />
            </FrameContainer>
        )
    )
}
