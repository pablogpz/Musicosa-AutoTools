import { eq } from 'drizzle-orm'
import { notFound } from 'next/navigation'

import FrameContainer from '@/app/components/FrameContainer'
import { templateFactory } from '@/app/templates/components/Template'
import db from '@/db/database'
import { entries, entriesStats } from '@/db/schema'

export default async function Page({
    searchParams,
}: {
    searchParams: Promise<{ [key: string]: string | string[] | undefined }>
}) {
    const { q } = await searchParams

    if (!q || typeof q !== 'string' || isNaN(Number(q))) notFound()

    const requestedSequenceNumber = parseInt(q)

    const entryIdSubquery = db
        .select({ entryId: entriesStats.entry })
        .from(entriesStats)
        .where(eq(entriesStats.rankingSequence, requestedSequenceNumber))
        .as('sq')
    const template = await db
        .select({ entryId: entries.id })
        .from(entries)
        .innerJoin(entryIdSubquery, eq(entries.id, entryIdSubquery.entryId))

    if (template.length == 0) notFound()

    const TemplateComponent = await templateFactory(template[0].entryId)

    return (
        TemplateComponent && (
            <FrameContainer>
                <TemplateComponent />
            </FrameContainer>
        )
    )
}
