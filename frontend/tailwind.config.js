/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        parchment: {
          50: '#FCFBF8',
          100: '#FAF7F0',
          200: '#F2ECE1',
          300: '#E8DEC9',
          400: '#D5C5A6',
          900: '#3A3226',
        },
        sage: {
          50: '#F4F7F5',
          100: '#E5EDE7',
          200: '#CBDBCF',
          500: '#52796F',
          600: '#3D5A52',
          700: '#2F453E',
          800: '#23342E',
        },
        ochre: {
          50: '#FDF9F3',
          100: '#FAF0E2',
          500: '#C87D55',
          600: '#B06840',
          700: '#8A4F30',
        },
        sattva: {
          light: '#E8F5E9',
          border: '#A5D6A7',
          DEFAULT: '#2E7D32',
          dark: '#1B5E20',
        },
        rajas: {
          light: '#FFF8E1',
          border: '#FFE082',
          DEFAULT: '#D97706',
          dark: '#B45309',
        },
        tamas: {
          light: '#F1F5F9',
          border: '#CBD5E1',
          DEFAULT: '#475569',
          dark: '#334155',
        },
      },
      fontFamily: {
        serif: ['"Playfair Display"', 'Georgia', 'serif'],
        sans: ['"Inter"', 'system-ui', '-apple-system', 'sans-serif'],
      },
      boxShadow: {
        'soft': '0 4px 20px -2px rgba(45, 90, 71, 0.06), 0 2px 6px -1px rgba(0, 0, 0, 0.04)',
        'card': '0 10px 30px -4px rgba(42, 59, 52, 0.08)',
      },
    },
  },
  plugins: [],
}
