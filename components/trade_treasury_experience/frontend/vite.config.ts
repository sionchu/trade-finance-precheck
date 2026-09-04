import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  base: "./",
  define: {
    "process.env.NODE_ENV": JSON.stringify("production"),
  },
  plugins: [react()],
  build: {
    outDir: "build",
    emptyOutDir: true,
    minify: "esbuild",
    cssCodeSplit: false,
    lib: {
      entry: "./src/index.tsx",
      formats: ["es"],
      fileName: () => "index.js",
    },
    rollupOptions: {
      output: {
        assetFileNames: (assetInfo) =>
          assetInfo.name?.endsWith(".css") ? "index.css" : "[name][extname]",
      },
    },
  },
});
