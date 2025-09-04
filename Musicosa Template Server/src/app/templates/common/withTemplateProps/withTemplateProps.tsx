import React from 'react'

import { TypedSetting } from '@/db/schema'
import settingsRepository from '@/db/repository/settings'

import { ResolvedTemplateProps, resolveTemplateProps } from './resolveTemplateProps'

export type TemplateSettingsProps = {
    scoreMinValue: number,
    scoreMaxValue: number
}

export default async function withTemplateProps<P extends object>(
    Component: React.ComponentType<P & TemplateSettingsProps & ResolvedTemplateProps>,
    templateUUID: string,
): Promise<React.ComponentType<P> | undefined> {
    const scoreMinValueSetting: TypedSetting<number> | undefined =
        await settingsRepository.getSettingByKey('validation.score_min_value')
    const scoreMaxValueSetting: TypedSetting<number> | undefined =
        await settingsRepository.getSettingByKey('validation.score_max_value')

    const templateProps = await resolveTemplateProps(templateUUID)
    if (!templateProps) return undefined

    return (props: P) =>
        <Component scoreMinValue={scoreMinValueSetting?.value ?? 0} scoreMaxValue={scoreMaxValueSetting?.value ?? 10}
                   {...templateProps} {...props}/>
}