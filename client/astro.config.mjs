import { defineConfig } from 'astro/config';

import tailwind from "@astrojs/tailwind";

// https://astro.build/config
export default defineConfig({
  output: "server",
  server: {
      headers: {
          "Access-Control-Allow-Origin": "*"
      }
  },
  integrations: [tailwind()]
});