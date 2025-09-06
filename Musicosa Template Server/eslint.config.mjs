import nextPlugin from "@next/eslint-plugin-next"
import reactPlugin from 'eslint-plugin-react'
import reactHooks from 'eslint-plugin-react-hooks'
import { defineConfig } from 'eslint/config'
import tseslint from 'typescript-eslint'

const { flatConfig: nextConfig } = nextPlugin

export default defineConfig([
    {
        files: ['src/**/*.{ts,tsx}'],
        extends: [
            tseslint.configs.recommended,
            reactPlugin.configs.flat.recommended,
            reactPlugin.configs.flat['jsx-runtime'],
            reactHooks.configs['recommended-latest'],
            nextConfig.recommended,
        ],
        rules: {
            'react/display-name': 'off',
            '@next/next/no-img-element': 'off',
        },
    },
])