import React from 'react'

import withTemplateProps from '@/app/templates/common/withTemplateProps'

import { editionTemplateFactory } from './7th-edition/editionTemplateFactory'

export default async function templateFactory(uuid: string): Promise<React.ComponentType | undefined> {
    const EditionTemplateComponent = await editionTemplateFactory(uuid)

    if (!EditionTemplateComponent) return undefined

    return withTemplateProps(EditionTemplateComponent, uuid)
}