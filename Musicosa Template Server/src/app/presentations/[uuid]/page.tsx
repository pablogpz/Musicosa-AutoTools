import { notFound } from 'next/navigation'

import db from '@/db/database'
import { entries } from '@/db/schema'

import presentationFactory from '@/app/presentations/components/Presentation/presentationFactory'
import FrameContainer from '@/app/components/FrameContainer'

type Params = { uuid: string }

export async function generateStaticParams(): Promise<Params[]> {
    const allEntriesUUIDs = await db.select({ uuid: entries.id }).from(entries)

    return allEntriesUUIDs.map(result => ({ uuid: result.uuid }))
}

export default async function Page({ params }: { params: Promise<Params> }) {
    const { uuid } = await params

    const PresentationComponent = await presentationFactory(uuid)

    if (!PresentationComponent)
        notFound()

    return (
        <FrameContainer>
            <PresentationComponent/>
        </FrameContainer>
    )
}
