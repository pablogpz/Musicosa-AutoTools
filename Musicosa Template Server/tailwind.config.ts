import type { Config } from 'tailwindcss'

export default {
    content: [
        './src/app/**/*.{js,ts,jsx,tsx}',
    ],
    theme: {
        fontFamily: {
            sans: ["system-ui", "sans-serif"],
        }
    },
    plugins: [],
} satisfies Config