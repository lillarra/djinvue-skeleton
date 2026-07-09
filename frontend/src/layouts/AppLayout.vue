<script setup>
// Layout réutilisable : toute page qui l'utilise hérite de la navbar et
// d'un conteneur centré/responsive. Voir frontend/src/pages/demo/Index.vue
// pour un exemple d'utilisation.
import Navbar from "../components/shared/Navbar.vue";
</script>

<template>
  <div class="min-h-screen bg-base-200">
    <Navbar />
    <main class="container mx-auto px-4 py-6">
      <slot />
    </main>
  </div>
</template>
