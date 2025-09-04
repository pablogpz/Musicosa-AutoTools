import React from 'react'

import withPresentationProps from '@/app/presentations/common/withPresentationProps'

import { Presentation } from './Presentation'

export default function presentationFactory(uuid: string): Promise<React.ComponentType | undefined> {
    return withPresentationProps(Presentation, uuid)
}