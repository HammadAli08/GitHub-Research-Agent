/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                background: "#ffffff",
                foreground: "#000000",
                muted: "#f4f4f5",
                "muted-foreground": "#71717a",
                border: "#e4e4e7",
                "accent-deep": "#4F5C78",
                "accent-primary": "#455B8F",
                "seafoam": "#458F81",
                "forest-dark": "#1C2926",
                "teal-dark": "#05262B",
                "slate-mist": "#5E7175",
            },
        },
    },
    plugins: [
        require('@tailwindcss/typography'),
    ],
}
