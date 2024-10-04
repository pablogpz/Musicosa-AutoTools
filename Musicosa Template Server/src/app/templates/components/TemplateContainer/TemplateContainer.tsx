import React, { PropsWithChildren } from 'react'

import settingsRepository from '@/db/repository/settings'
import { DEFAULT_TEMPLATE_HEIGHT, DEFAULT_TEMPLATE_WIDTH } from '@/app/defaults'

import BaseTemplateContainer from './BaseTemplateContainer'

export default async function TemplateContainer({ children }: PropsWithChildren) {
    const widthSetting = await settingsRepository.getSettingByKey<number>('templates.total_width_px')
    const width = widthSetting?.value ?? DEFAULT_TEMPLATE_WIDTH

    const heightSetting = await settingsRepository.getSettingByKey<number>('templates.total_height_px')
    const height = heightSetting?.value ?? DEFAULT_TEMPLATE_HEIGHT

    return (
        <BaseTemplateContainer width={width} height={height}>
            {children}
        </BaseTemplateContainer>
    )
}