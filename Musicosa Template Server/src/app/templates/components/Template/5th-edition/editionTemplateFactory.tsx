import React from 'react'

import entriesRepository from '@/db/repository/5th-edition/entries'
import { ResolvedTemplateProps } from '@/app/templates/common/withTemplateProps'
import settingsRepository from '@/db/repository/settings'
import { TypedSetting } from '@/db/schema'
import { Template } from '@/app/templates/components/Template/5th-edition/Template'

import { defaultEditionProps } from './defaults'

export async function editionTemplateFactory(entryUUID: string): Promise<React.FC<ResolvedTemplateProps> | undefined> {
    const scoreMinValueSetting: TypedSetting<number> | undefined =
        await settingsRepository.getSettingByKey('validation.score_min_value')
    const scoreMaxValueSetting: TypedSetting<number> | undefined =
        await settingsRepository.getSettingByKey('validation.score_max_value')

    const sequenceNumberInSpecialTopic = await entriesRepository.getEntrySequenceNumberInSpecialTopic(entryUUID)

    return (props: ResolvedTemplateProps) =>
        <Template {...props}
                  scoreMinValue={scoreMinValueSetting?.value ?? defaultEditionProps.scoreMinValue}
                  scoreMaxValue={scoreMaxValueSetting?.value ?? defaultEditionProps.scoreMaxValue}
                  sequenceNumberInSpecialTopic={sequenceNumberInSpecialTopic}/>
}