/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./**/templates/*.html', './**/templates/**/*.html'],
  theme: {
    extend: {
      colors: {
        'lapiz': {
          50: "#f4f4fb",
          100: "#e9eaf5",
          200: "#ced2e9",
          300: "#a2abd7",
          400: "#707ec0",
          500: "#4e5ea9",
          600: "#3c488d",
          700: "#313a73",
          800: "#2c3360",
          900: "#292d51",
          950: "#0c0d18"
        }
      }
    },
  },
  plugins: [],
}

