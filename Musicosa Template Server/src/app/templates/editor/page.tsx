import React from 'react'

import settingsRepository from '@/db/repository/settings'
import { DEFAULT_DECIMAL_DIGITS, DEFAULT_TEMPLATE_HEIGHT, DEFAULT_TEMPLATE_WIDTH } from '@/app/defaults'

import TemplateEditor from '@/app/templates/components/4th-edition/TemplateEditor'

export default async function Page() {
    const widthSetting = await settingsRepository.getSettingByKey<number>('templates.total_width_px')
    const width = widthSetting?.value ?? DEFAULT_TEMPLATE_WIDTH

    const heightSetting = await settingsRepository.getSettingByKey<number>('templates.total_height_px')
    const height = heightSetting?.value ?? DEFAULT_TEMPLATE_HEIGHT

    const decimalDigitsSetting = await settingsRepository.getSettingByKey<number>('ranking.significant_decimal_digits')
    const decimalDigits = decimalDigitsSetting?.value ?? DEFAULT_DECIMAL_DIGITS

    return <TemplateEditor templateWidth={width} templateHeight={height} decimalDigits={decimalDigits}/>
}

