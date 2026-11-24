// Import Vite helper.
import { defineConfig } from "vite";

// Import React plugin.
import react from "@vitejs/plugin-react";


// Export Vite configuration.
export default defineConfig({

  // Enable React support.
  plugins: [
    react(),
  ],

  // Development server.
  server: {

    // Frontend port.
    port: 3000,

    // Allow local network access.
    host: true,
  },
});