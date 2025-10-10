import { dirname } from "path";
import { fileURLToPath } from "url";
import { FlatCompat } from "@eslint/eslintrc";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const compat = new FlatCompat({
  baseDirectory: __dirname,
});

const eslintConfig = [
  // Configuración base de Next + TypeScript
  ...compat.extends("next/core-web-vitals", "next/typescript"),

  // Ignorar carpetas de build, node_modules, etc.
  {
    ignores: [
      "node_modules/**",
      ".next/**",
      "out/**",
      "build/**",
      "next-env.d.ts",
    ],
  },

  // 👇 Aquí agregas tus reglas personalizadas
  {
    rules: {
      "react/prop-types": "off",
    },
  },
];

export default eslintConfig;
