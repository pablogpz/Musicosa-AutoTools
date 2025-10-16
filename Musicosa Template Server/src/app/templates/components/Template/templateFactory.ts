import React from 'react'

import withTemplateProps from '@/app/templates/common/withTemplateProps'

import Template, { TemplateOuterProps } from './Template'

export function templateFactory(templateId: string): Promise<React.ComponentType<TemplateOuterProps> | undefined> {
    return withTemplateProps<TemplateOuterProps>(Template, templateId)
}
