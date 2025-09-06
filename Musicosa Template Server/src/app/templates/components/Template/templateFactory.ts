import React from 'react'

import withTemplateProps from '@/app/templates/common/withTemplateProps'

import Template from './Template'

export function templateFactory(templateId: string): Promise<React.ComponentType | undefined> {
    return withTemplateProps(Template, templateId)
}
