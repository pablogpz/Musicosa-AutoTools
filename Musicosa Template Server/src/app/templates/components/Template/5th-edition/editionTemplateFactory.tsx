import React from 'react'

import entriesRepository from '@/db/repository/5th-edition/entries'
import { ResolvedTemplateProps } from '@/app/templates/common/withTemplateProps'
import { Template } from '@/app/templates/components/Template/5th-edition/Template'

export async function editionTemplateFactory(entryUUID: string): Promise<React.FC<ResolvedTemplateProps> | undefined> {
    const sequenceNumberInSpecialTopic = await entriesRepository.getEntrySequenceNumberInSpecialTopic(entryUUID)

    return (props: ResolvedTemplateProps) =>
        <Template {...props} sequenceNumberInSpecialTopic={sequenceNumberInSpecialTopic}/>
}