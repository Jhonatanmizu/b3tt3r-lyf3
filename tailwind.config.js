/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./**/templates/**/*.html",
    "./**/*.py",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          DEFAULT: "#66CCAA",
          secondary: "#2DD4BF",
        },
        surface: {
          dark: "#1E293B",
        },
        bg: {
          dark: "#0F1115",
        },
      },
      fontFamily: {
        primary: ["Inter", "sans-serif"],
      },
    },
  },
  plugins: [],
}
