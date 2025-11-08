/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'dark-bg': '#0a0a0f',
        'dark-card': '#12121a',
        'dark-hover': '#1a1a24',
        'dark-border': '#252530',
        'agent-primary': '#3b82f6',
        'agent-secondary': '#8b5cf6',
        'tool-primary': '#10b981',
        'tool-secondary': '#059669',
        'workflow-primary': '#f59e0b',
        'workflow-secondary': '#d97706',
        'solution-primary': '#ec4899',
        'solution-secondary': '#db2777',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
