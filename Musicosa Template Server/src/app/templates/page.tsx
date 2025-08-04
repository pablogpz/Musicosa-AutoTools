import { notFound } from 'next/navigation'
import { eq } from 'drizzle-orm'

import db from '@/db/database'
import { entries, entriesStats } from '@/db/schema'
import templateFactory from '@/app/templates/components/Template/templateFactory'
import FrameContainer from '@/app/components/FrameContainer'

export default async function Page(
    {
        searchParams
    }: {
        searchParams: { [key: string]: string | string[] | undefined }
    }) {

    if (!searchParams["q"] || typeof searchParams["q"] !== "string" || isNaN(Number(searchParams["q"])))
        notFound()

    const requestedSequenceNumber = parseInt(searchParams["q"])

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

