// Point d'entrée unique du frontend : c'est ce fichier que Vite sert (en
// dev) ou buildе (en prod), et que config/templates/base.html charge via
// {% vite_asset %}.
import "./css/app.css";
import { createApp, h } from "vue";
import { createInertiaApp } from "@inertiajs/vue3";

// IMPORTANT : @inertiajs/vue3 v3 attend la page initiale dans une balise
// <script data-page="app" type="application/json">, alors que le paquet
// Python inertia-django ne génère nativement que <div data-page="...">
// (protocole v1/v2). On comble cet écart via une surcharge de template
// (config/templates/inertia.html + apps/accounts/templatetags/inertia_extras.py).
// Voir le README, section "Pièges connus", avant toute mise à jour de
// @inertiajs/vue3 ou d'inertia-django.

createInertiaApp({
  // Résout le nom de composant renvoyé par Django (ex: "demo/Index") vers
  // le fichier .vue correspondant dans frontend/src/pages/. Le nom envoyé
  // par Django (ex: apps/demo/views.py -> @inertia("demo/Index")) doit
  // correspondre exactement au chemin en minuscules ci-dessous : c'est le
  // miroir de nommage entre apps Django et dossiers de pages.
  resolve: (name) => {
    const pages = import.meta.glob("./pages/**/*.vue", { eager: true });
    return pages[`./pages/${name}.vue`];
  },
  setup({ el, App, props, plugin }) {
    createApp({ render: () => h(App, props) })
      .use(plugin)
      .mount(el);
  },
});
