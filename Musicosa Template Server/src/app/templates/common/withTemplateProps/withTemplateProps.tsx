import React from 'react'

import settingsRepository from '@/db/repositories/settings'

import { defaultTemplateSettingsProps } from './defaults'
import { ResolvedTemplateProps, resolveTemplateProps } from './resolveTemplateProps'

export type TemplateSettingsProps = {
    scoreMinValue: number
    scoreMaxValue: number
}

export default async function withTemplateProps<P extends object>(
    Component: React.ComponentType<P & TemplateSettingsProps & ResolvedTemplateProps>,
    templateId: string
): Promise<React.ComponentType<P> | undefined> {
    const templateProps = await resolveTemplateProps(templateId)
    if (!templateProps) return undefined

    const scoreMinValueSetting = await settingsRepository.getSettingByKey<number>('validation.score_min_value')
    const scoreMaxValueSetting = await settingsRepository.getSettingByKey<number>('validation.score_max_value')

    return (props: P) => (
        <Component
            scoreMinValue={scoreMinValueSetting?.value ?? defaultTemplateSettingsProps.scoreMinValue}
            scoreMaxValue={scoreMaxValueSetting?.value ?? defaultTemplateSettingsProps.scoreMaxValue}
            {...templateProps}
            {...props}
        />
    )
}
