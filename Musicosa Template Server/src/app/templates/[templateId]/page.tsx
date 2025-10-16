import { notFound } from 'next/navigation'

import FrameContainer from '@/app/components/FrameContainer'
import { templateFactory } from '@/app/templates/components/Template'
import db from '@/db/database'
import { templates } from '@/db/schema'

type Params = { templateId: string }
type SearchParams = { disableVideoPlaceholder: string }

export async function generateStaticParams(): Promise<Params[]> {
    const templateIDs = await db.select({ id: templates.nomination }).from(templates)

    return templateIDs.map((result) => ({ templateId: result.id }))
}

export default async function Page({
    params,
    searchParams,
}: {
    params: Promise<Params>
    searchParams: Promise<SearchParams>
}) {
    const { templateId } = await params
    const { disableVideoPlaceholder } = await searchParams

    const TemplateComponent = await templateFactory(templateId)

    if (!TemplateComponent) notFound()

    const videoPlaceholderDisabled = disableVideoPlaceholder === 'true'

    return (
        <FrameContainer>
            <TemplateComponent disableVideoPlaceholder={videoPlaceholderDisabled} />
        </FrameContainer>
    )
}
