import React from 'react'

import { ResolvedTemplateProps, resolveTemplateProps } from './resolveTemplateProps'

export default async function withTemplateProps<P extends object>(
    Component: React.ComponentType<P & ResolvedTemplateProps>,
    templateUUID: string,
): Promise<React.ComponentType<P> | undefined> {
    const templateProps = await resolveTemplateProps(templateUUID)

    if (!templateProps) return undefined
    return (props: P) => <Component {...templateProps} {...props}/>
}