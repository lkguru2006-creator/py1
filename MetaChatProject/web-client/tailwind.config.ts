

import type { Config } from "tailwindcss";

const config: Config = {
    content: [
        "./pages/**/*.{js,ts,jsx,tsx,mdx}",
        "./components/**/*.{js,ts,jsx,tsx,mdx}",
        "./app/**/*.{js,ts,jsx,tsx,mdx}",
    ],
    theme: {
        extend: {
            colors: {
                meta: {
                    base: "#0064E0", // Classic Meta Blue
                    dark: "#004DAD",
                    light: "#1877F2",
                    surface: "#EBF5FF",
                },
                aesthetic: {
                    50: "#f0f9ff",
                    100: "#e0f2fe",
                    200: "#bae6fd",
                    300: "#7dd3fc",
                    400: "#38bdf8",
                    500: "#0ea5e9", // Sky blue for vibrant gradients
                    600: "#0284c7",
                    700: "#0369a1",
                    800: "#075985",
                    900: "#0c4a6e",
                },
                glass: {
                    border: "rgba(255, 255, 255, 0.2)",
                    surface: "rgba(255, 255, 255, 0.1)",
                    highlight: "rgba(255, 255, 255, 0.5)",
                }
            },
            backgroundImage: {
                "gradient-radial": "radial-gradient(var(--tw-gradient-stops))",
                "gradient-conic": "conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))",
                "meta-gradient": "linear-gradient(135deg, #0064E0 0%, #00C6FF 100%)",
                "deep-blue": "linear-gradient(to bottom, #0f172a, #1e293b)",
            },
            animation: {
                "float": "float 6s ease-in-out infinite",
                "spin-slow": "spin 8s linear infinite",
            },
            keyframes: {
                float: {
                    "0%, 100%": { transform: "translateY(0)" },
                    "50%": { transform: "translateY(-20px)" },
                },
            },
        },
    },
    plugins: [],
};
