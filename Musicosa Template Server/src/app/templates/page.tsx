import { notFound } from 'next/navigation'
import { eq } from 'drizzle-orm'

import db from '@/db/database'
import { entries, entriesStats } from '@/db/schema'
import { templateFactory } from '@/app/templates/components/Template'
import FrameContainer from '@/app/components/FrameContainer'

export default async function Page({ searchParams }: {
    searchParams: Promise<{ [key: string]: string | string[] | undefined }>
}) {
    const { q } = await searchParams

    if (!q || typeof q !== "string" || isNaN(Number(q)))
        notFound()

    const requestedSequenceNumber = parseInt(q)

    const entryIdSubquery = db
        .select({ entryId: entriesStats.entry })
        .from(entriesStats)
        .where(eq(entriesStats.rankingSequence, requestedSequenceNumber))
        .as("sq")
    const template = await db
        .select({ entryId: entries.id })
        .from(entries)
        .innerJoin(entryIdSubquery, eq(entries.id, entryIdSubquery.entryId))

    if (!template.length)
        notFound()

    const TemplateComponent = await templateFactory(template[0].entryId)

    return TemplateComponent && (
        <FrameContainer>
            <TemplateComponent/>
        </FrameContainer>
    )
}

