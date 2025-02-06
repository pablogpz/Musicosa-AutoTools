import { notFound } from 'next/navigation'
import { and, eq } from 'drizzle-orm'

import db from '@/db/database'
import { nominations, nominationStats } from '@/db/schema'
import templateFactory from '@/app/templates/components/Template/templateFactory'
import TemplateContainer from '@/app/templates/components/TemplateContainer'

export default async function Page(
    {
        searchParams
    }: {
        searchParams: { [key: string]: string | string[] | undefined }
    }) {

    if (!searchParams["award"] || typeof searchParams["award"] !== "string")
        notFound()
    if (!searchParams["q"] || typeof searchParams["q"] !== "string" || isNaN(Number(searchParams["q"])))
        notFound()

    const requestedAward = searchParams["award"]
    const requestedSequenceNumber = parseInt(searchParams["q"])

    const nominationsIdSubquery = db
        .select({ nominationId: nominations.id })
        .from(nominations)
        .innerJoin(nominationStats, eq(nominationStats.nomination, nominations.id))
        .where(and(eq(nominations.award, requestedAward), eq(nominationStats.rankingSequence, requestedSequenceNumber)))
        .as("sq")
    const template = await db
        .select({ nominationId: nominations.id })
        .from(nominations)
        .innerJoin(nominationsIdSubquery, eq(nominations.id, nominationsIdSubquery.nominationId))

    if (!template.length)
        notFound()

    const TemplateComponent = await templateFactory(template[0].nominationId)

    return TemplateComponent && (
        <TemplateContainer>
            <TemplateComponent/>
        </TemplateContainer>
    )
}

