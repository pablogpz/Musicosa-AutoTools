import { notFound } from 'next/navigation'

import db from '@/db/database'
import { templates } from '@/db/schema'

import { templateFactory } from '@/app/templates/components/Template'
import FrameContainer from '@/app/components/FrameContainer'

type Params = { templateId: string }

export async function generateStaticParams(): Promise<Params[]> {
    const templateIDs = await db.select({ id: templates.entry }).from(templates)

    return templateIDs.map(result => ({ templateId: result.id }))
}

export default async function Page({ params }: { params: Promise<Params> }) {
    const { templateId } = await params

    const TemplateComponent = await templateFactory(templateId)

    if (!TemplateComponent)
        notFound()

    return (
        <FrameContainer>
            <TemplateComponent/>
        </FrameContainer>
    )
}

