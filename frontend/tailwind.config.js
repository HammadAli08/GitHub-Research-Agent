/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                background: "#0a0a0f",
                foreground: "#ffffff",
                muted: "#1e293b",
                "muted-foreground": "#94a3b8",
                border: "#334155",
                "royal-main": "#0a0a0f",      // Deepest black
                "royal-secondary": "#111118", // Panel background
                "accent-gold": "#D4AF37",     // Metallic Gold
                "accent-gold-dim": "#8A7224", // Muted Gold
                "regal-blue": "#1e293b",      // Deep slate/blue
                "noble-slate": "#cbd5e1",     // Text color
            },
        },
    },
    plugins: [
        require('@tailwindcss/typography'),
    ],
}
