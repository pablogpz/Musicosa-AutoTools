import React from 'react'

import { ResolvedPresentationProps, resolvePresentationProps } from './resolvePresentationProps'

export default async function withPresentationProps<P extends object>(
    Component: React.ComponentType<P & ResolvedPresentationProps>,
    nominationUUID: string,
): Promise<React.ComponentType<P> | undefined> {
    const presentationProps = await resolvePresentationProps(nominationUUID)

    if (!presentationProps) return undefined
    return (props: P) => <Component {...presentationProps} {...props}/>
}