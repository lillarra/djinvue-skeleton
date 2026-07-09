// Config Vite du projet. Le rôle de Vite ici est double :
//  - en dev : servir frontend/src/entry.js avec Hot Module Replacement
//    (HMR) sur http://localhost:5173, lu par Django via django-vite ;
//  - en prod : construire (`npm run build`) un bundle buildé dans
//    frontend/dist/, accompagné d'un manifest.json que django-vite lit pour
//    savoir quels fichiers (hashés) injecter dans le HTML.
import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  plugins: [vue(), tailwindcss()],

  // Les URLs générées dans le manifest sont préfixées par /static/, qui
  // correspond à STATIC_URL côté Django.
  base: "/static/",

  build: {
    // Dossier de sortie du build, lu par STATICFILES_DIRS et par
    // DJANGO_VITE (manifest_path) dans config/settings.py.
    outDir: "frontend/dist",
    emptyOutDir: true,
    manifest: true,
    rollupOptions: {
      input: "frontend/src/entry.js",
    },
  },

  server: {
    host: "localhost",
    port: 5173,
    // Nécessaire pour que le navigateur charge bien les assets depuis le
    // serveur de dev Vite (et pas depuis Django) quand dev_mode est actif.
    origin: "http://localhost:5173",
    // La page est servie par Django (localhost:8500) mais charge les
    // scripts (type="module") depuis Vite (localhost:5173) : c'est une
    // origine différente. Un script module cross-origin est chargé en
    // mode CORS par le navigateur, qui le bloque sans cet en-tête.
    cors: true,
  },
});
