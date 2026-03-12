/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // 末世主题色
        apocalypse: {
          bg: '#0a0a0f',
          card: '#12121a',
          border: '#1e1e2e',
          text: '#e0e0e0',
          muted: '#6b6b7b',
          danger: '#ff4757',
          warning: '#ffa502',
          success: '#2ed573',
        }
      }
    },
  },
  plugins: [],
}
