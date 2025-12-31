/** @type {import('tailwindcss').Config} */
module.exports = {
  theme: {
    extend: {
      colors: {
        brand: {
          primary: {
            50: "#f0f7ff",
            100: "#e0f0fe",
            200: "#bae4fd",
            300: "#7dd3fc",
            400: "#38bdf8",
            500: "#0ea5e9",
            600: "#0284c7",
            700: "#0369a1",
            800: "#075985",
            900: "#0c3d66",
            950: "#082f49",
          },
          teal: {
            50: "#f0fdfa",
            100: "#ccfbf1",
            500: "#14b8a6",
            600: "#0d9488",
            700: "#0f766e",
          },
          emerald: {
            50: "#f0fdf4",
            500: "#22c55e",
            600: "#16a34a",
            700: "#15803d",
          },
          purple: {
            50: "#faf5ff",
            500: "#a855f7",
            600: "#9333ea",
            700: "#7e22ce",
          },
        },
        semantic: {
          success: {
            50: "#f0fdf4",
            500: "#10b981",
            600: "#059669",
          },
          warning: {
            50: "#fffbeb",
            500: "#f59e0b",
            600: "#d97706",
          },
          error: {
            50: "#fef2f2",
            500: "#ef4444",
            600: "#dc2626",
          },
          info: {
            50: "#eff6ff",
            500: "#3b82f6",
            600: "#2563eb",
          },
        },
        severity: {
          critical: "#d31313",
          high: "#ef4444",
          moderate: "#eab308",
          low: "#0ea5e9",
          normal: "#22c55e",
        },
      },
      fontFamily: {
        heading: ["Pretendard", "Inter", "system-ui", "sans-serif"],
        body: ["Pretendard", "Inter", "system-ui", "sans-serif"],
        mono: ["JetBrains Mono", "Fira Code", "monospace"],
      },
      fontSize: {
        xs: ["0.75rem", { lineHeight: "1rem" }],
        sm: ["0.875rem", { lineHeight: "1.25rem" }],
        base: ["1rem", { lineHeight: "1.5rem" }],
        lg: ["1.125rem", { lineHeight: "1.75rem" }],
        xl: ["1.25rem", { lineHeight: "1.75rem" }],
        "2xl": ["1.5rem", { lineHeight: "2rem" }],
        "3xl": ["1.875rem", { lineHeight: "2.25rem" }],
        "4xl": ["2.25rem", { lineHeight: "2.5rem" }],
        "5xl": ["3rem", { lineHeight: "1" }],
      },
      borderRadius: {
        none: "0",
        sm: "0.25rem",
        DEFAULT: "0.5rem",
        md: "0.5rem",
        lg: "1rem",
        xl: "1.5rem",
        full: "9999px",
      },
      boxShadow: {
        sm: "0 1px 2px 0 rgb(0 0 0 / 0.05)",
        DEFAULT:
          "0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)",
        md: "0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)",
        lg: "0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)",
        xl: "0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)",
      },
      transitionDuration: {
        instant: "0ms",
        fast: "150ms",
        DEFAULT: "250ms",
        slow: "350ms",
        slower: "500ms",
      },
      transitionTimingFunction: {
        standard: "cubic-bezier(0.4, 0, 0.2, 1)",
        entrance: "cubic-bezier(0, 0, 0.2, 1)",
        exit: "cubic-bezier(0.4, 0, 1, 1)",
        emphasis: "cubic-bezier(0.4, 0, 0.6, 1)",
      },
      zIndex: {
        base: "0",
        dropdown: "100",
        sticky: "200",
        modal: "300",
        toast: "400",
        "critical-alert": "500",
      },
      animation: {
        "fade-in": "fadeIn 250ms ease-out",
        "slide-up": "slideUp 250ms ease-out",
        "pulse-slow": "pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite",
      },
      keyframes: {
        fadeIn: {
          "0%": { opacity: "0" },
          "100%": { opacity: "1" },
        },
        slideUp: {
          "0%": { transform: "translateY(10px)", opacity: "0" },
          "100%": { transform: "translateY(0)", opacity: "1" },
        },
      },
    },
  },
  plugins: [],
};
