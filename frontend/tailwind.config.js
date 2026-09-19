/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./login.html",
    "./register.html",
    "./browse-teams.html",
    "./dashboard.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        canvas: {
          DEFAULT: '#FAF8F5',
          alt: '#F4EFEA',
          card: '#FFFFFF',
          border: '#E4DDD3',
          borderHover: '#CEBFB0'
        },
        terracotta: {
          DEFAULT: '#C2410C',
          hover: '#9A3412',
          light: '#FDF2EC',
          border: '#F6D5C3'
        },
        ochre: {
          DEFAULT: '#B45309',
          light: '#FEF3C7',
          border: '#FDE68A'
        },
        ink: {
          DEFAULT: '#1C1917',
          secondary: '#3D3835',
          muted: '#6B6560',
          subtle: '#9A938C'
        },
        sage: {
          DEFAULT: '#365314',
          light: '#F2F6EC',
          border: '#D7E5C3'
        }
      },
      fontFamily: {
        heading: ['"Outfit"', 'system-ui', 'sans-serif'],
        body: ['"Plus Jakarta Sans"', 'system-ui', 'sans-serif'],
        mono: ['"Space Mono"', 'monospace']
      }
    },
  },
  plugins: [],
}
