import React from 'react'

import withPresentationProps from '@/app/presentations/common/withPresentationProps'

import Presentation from './Presentation'

export function presentationFactory(nominationId: string): Promise<React.ComponentType | undefined> {
    return withPresentationProps(Presentation, nominationId)
}
