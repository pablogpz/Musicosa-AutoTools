import React from 'react'

import { ResolvedPresentationProps, resolvePresentationProps } from './resolvePresentationProps'

export default async function withPresentationProps<P extends object>(
    Component: React.ComponentType<P & ResolvedPresentationProps>,
    entryId: string,
): Promise<React.ComponentType<P> | undefined> {
    const presentationProps = await resolvePresentationProps(entryId)

    if (!presentationProps) return undefined
    return (props: P) => <Component {...presentationProps} {...props}/>
}