import { notFound } from 'next/navigation'

import FrameContainer from '@/app/components/FrameContainer'
import { presentationFactory } from '@/app/presentations/components/Presentation'
import db from '@/db/database'
import { nominations } from '@/db/schema'

type Params = { nominationId: string }

export async function generateStaticParams(): Promise<Params[]> {
    const nominationIDs = await db.select({ id: nominations.id }).from(nominations)

    return nominationIDs.map((result) => ({ nominationId: result.id }))
}

export default async function Page({ params }: { params: Promise<Params> }) {
    const { nominationId } = await params

    const PresentationComponent = await presentationFactory(nominationId)

    if (!PresentationComponent) notFound()

    return (
        <FrameContainer>
            <PresentationComponent />
        </FrameContainer>
    )
}
