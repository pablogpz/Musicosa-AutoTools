import React from 'react'

import settingsRepository from '@/db/repository/settings'
import { DEFAULT_DISPLAY_DECIMAL_DIGITS, DEFAULT_TEMPLATE_HEIGHT, DEFAULT_TEMPLATE_WIDTH } from '@/app/defaults'

import TemplateEditor from '@/app/templates/components/TemplateEditor'

export default async function Page() {
    const widthSetting = await settingsRepository.getSettingByKey<number>('templates.total_width_px')
    const width = widthSetting?.value ?? DEFAULT_TEMPLATE_WIDTH

    const heightSetting = await settingsRepository.getSettingByKey<number>('templates.total_height_px')
    const height = heightSetting?.value ?? DEFAULT_TEMPLATE_HEIGHT

    const displayDecimalDigitsSetting = await settingsRepository.getSettingByKey<number>('templates.display_decimal_digits')
    const displayDecimalDigits = displayDecimalDigitsSetting?.value ?? DEFAULT_DISPLAY_DECIMAL_DIGITS

    return <TemplateEditor templateWidth={width} templateHeight={height} displayDecimalDigits={displayDecimalDigits}/>
}
