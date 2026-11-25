import { defineConfig } from "vitest/config";

export default defineConfig({
  esbuild: { jsx: "automatic" },
  test: {
    globals: true,
    environmentMatchGlobs: [["apps/web/**", "jsdom"]],
    setupFiles: ["./vitest.setup.ts"],
  },
});
