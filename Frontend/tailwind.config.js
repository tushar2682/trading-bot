/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        "elite-dark": "#0a0a0b",
        "elite-charcoal": "#121214",
        "elite-gray": "#1c1c1e",
        "elite-accent": "#3a3a3c",
        "elite-blue": "#0A84FF",
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [require("daisyui")],
  daisyui: {
    themes: [
      {
        businessElite: {
          "primary": "#0A84FF",
          "secondary": "#5e5ce6",
          "accent": "#bf5af2",
          "neutral": "#1c1c1e",
          "base-100": "#0a0a0b",
          "info": "#0a84ff",
          "success": "#30d158",
          "warning": "#ffd60a",
          "error": "#ff453a",
        },
      },
      "dark",
    ],
  },
}
