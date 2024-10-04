import React from 'react'

import withTemplateProps from '@/app/templates/common/withTemplateProps'

import { Template } from './Template'

export default function templateFactory(uuid: string): Promise<React.ComponentType | undefined> {
    return withTemplateProps(Template, uuid)
}