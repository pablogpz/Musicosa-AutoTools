export enum SettingsGroups {
    validation = 'validation',
    frame = 'frame',
    templates = 'templates',
    ranking = 'ranking'
}

export enum ValidationSettingsNames {
    scoreMinValue = 'score_min_value',
    scoreMaxValue = 'score_max_value',
}

export enum FrameSettingsNames {
    widthPx = 'width_px',
    heightPx = 'height_px',
}

export enum TemplatesSettingsNames {
    displayDecimalDigits = "display_decimal_digits",
}

export enum RankingSettingsNames {
    significantDecimalDigits = 'significant_decimal_digits'
}

export type SettingsKey =
    `${SettingsGroups.validation}.${ValidationSettingsNames}`
    | `${SettingsGroups.frame}.${FrameSettingsNames}`
    | `${SettingsGroups.templates}.${TemplatesSettingsNames}`
    | `${SettingsGroups.ranking}.${RankingSettingsNames}`