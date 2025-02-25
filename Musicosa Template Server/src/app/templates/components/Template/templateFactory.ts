import React from 'react'

import withTemplateProps from '@/app/templates/common/withTemplateProps'

import { Template } from './TFA-2/Template'

export default function templateFactory(uuid: string): Promise<React.ComponentType | undefined> {
    return withTemplateProps(Template, uuid)
}