export enum SettingsGroups {
    validation = 'validation',
    templates = 'templates',
    ranking = 'ranking'
}

export enum ValidationSettingsNames {
    scoreMinValue = 'score_min_value',
    scoreMaxValue = 'score_max_value',
}

export enum RankingSettingsNames {
    significantDecimalDigits = 'significant_decimal_digits'
}

export enum TemplatesSettingsNames {
    totalWidthPx = 'total_width_px',
    totalHeightPx = 'total_height_px',
    displayDecimalDigits = "display_decimal_digits",
}

export type SettingsKey =
    `${SettingsGroups.validation}.${ValidationSettingsNames}`
    | `${SettingsGroups.ranking}.${RankingSettingsNames}`
    | `${SettingsGroups.templates}.${TemplatesSettingsNames}`
