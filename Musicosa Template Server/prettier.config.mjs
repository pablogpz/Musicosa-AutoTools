/**
 * @type {import('prettier').Config & import('@trivago/prettier-plugin-sort-imports').PluginConfig}
 */
const config = {
    printWidth: 120,
    tabWidth: 4,
    useTabs: false,
    semi: false,
    singleQuote: true,
    quoteProps: 'as-needed',
    jsxSingleQuote: true,
    trailingComma: 'es5',
    bracketSpacing: true,
    objectWrap: 'preserve',
    bracketSameLine: false,
    arrowParens: 'always',
    proseWrap: 'always',
    htmlWhitespaceSensitivity: 'strict',
    endOfLine: 'auto',
    embeddedLanguageFormatting: 'auto',
    singleAttributePerLine: true,
    plugins: ['@trivago/prettier-plugin-sort-imports'],
    importOrder: [
        // 1) third-party packages (scoped and unscoped)
        '^@?\\w',
        // 2) path-alias imports
        '^@/',
        // 3) same-directory and index
        '^\\./(?=.*/)(?!/?$)',
        '^\\.(?!/?$)',
        '^\\./?$',
    ],
    importOrderSeparation: true,
    importOrderSortSpecifiers: true,
    importOrderSideEffects: true,
}

export default config
