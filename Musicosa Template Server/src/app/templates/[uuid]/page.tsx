import { notFound } from 'next/navigation'

import db from '@/db/database'
import { nominations } from '@/db/schema'

import templateFactory from '@/app/templates/components/Template/templateFactory'
import TemplateContainer from '@/app/templates/components/TemplateContainer'

type Params = { uuid: string }

export async function generateStaticParams(): Promise<Params[]> {
    const allNominationsUUIDs = await db.select({ uuid: nominations.id }).from(nominations)

    return allNominationsUUIDs.map(result => ({ uuid: result.uuid }))
}

export default async function Page({ params }: { params: Params }) {
    const TemplateComponent = await templateFactory(params.uuid)

    if (!TemplateComponent)
        notFound()

    return (
        <TemplateContainer>
            <TemplateComponent/>
        </TemplateContainer>
    )
}

