import React from 'react'

import entriesRepository from '@/db/repository/4th-edition/entries'
import { ResolvedTemplateProps } from '@/app/templates/common/withTemplateProps'
import { Template } from '@/app/templates/components/Template/4th-edition/Template'
import settingsRepository from '@/db/repository/settings'
import { TypedSetting } from '@/db/schema'

export async function editionTemplateFactory(entryUUID: string): Promise<React.FC<ResolvedTemplateProps> | undefined> {
    const scoreMinValueSetting: TypedSetting<number> | undefined =
        await settingsRepository.getSettingByKey('validation.score_min_value')
    const scoreMaxValueSetting: TypedSetting<number> | undefined =
        await settingsRepository.getSettingByKey('validation.score_max_value')

    const sequenceNumberInAuthorEntries = await entriesRepository.getEntrySequenceNumberInAuthorEntries(entryUUID)
    if (!sequenceNumberInAuthorEntries) return undefined

    const sequenceNumberInSpecialTopic = await entriesRepository.getEntrySequenceNumberInSpecialTopic(entryUUID)

    const avgScoreDelta = await entriesRepository.getAvgScoreDeltaWithPreviousEntry(entryUUID)
    if (avgScoreDelta === undefined) return undefined

    return (props: ResolvedTemplateProps) =>
        <Template {...props}
                  scoreMinValue={scoreMinValueSetting?.value ?? 0}
                  scoreMaxValue={scoreMaxValueSetting?.value ?? 10}
                  sequenceNumberInAuthorEntries={sequenceNumberInAuthorEntries}
                  sequenceNumberInSpecialTopic={sequenceNumberInSpecialTopic}
                  avgScoreDelta={avgScoreDelta}/>
}