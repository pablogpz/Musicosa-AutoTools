import { notFound } from 'next/navigation'

import FrameContainer from '@/app/components/FrameContainer'
import { presentationFactory } from '@/app/presentations/components/Presentation'
import db from '@/db/database'
import { entries } from '@/db/schema'

type Params = { entryId: string }

export async function generateStaticParams(): Promise<Params[]> {
    const entryIDs = await db.select({ id: entries.id }).from(entries)

    return entryIDs.map((result) => ({ entryId: result.id }))
}

export default async function Page({ params }: { params: Promise<Params> }) {
    const { entryId } = await params

    const PresentationComponent = await presentationFactory(entryId)

    if (!PresentationComponent) notFound()

    return (
        <FrameContainer>
            <PresentationComponent />
        </FrameContainer>
    )
}
