<script setup>
// Page publique : prouve la chaîne complète Django -> Inertia -> Vue ->
// PostgreSQL. Les notes arrivent en prop directement depuis demo/views.py,
// aucune requête AJAX manuelle n'est nécessaire.
import AppLayout from "../../Layouts/AppLayout.vue";

defineProps({
  notes: { type: Array, default: () => [] },
});

function formatDate(iso) {
  return new Date(iso).toLocaleDateString("fr-FR", {
    day: "numeric",
    month: "long",
    year: "numeric",
  });
}
</script>

<template>
  <AppLayout>
    <h1 class="mb-2 text-2xl font-bold">Notes (démo Django → Inertia → Vue → PostgreSQL)</h1>
    <p class="mb-6 text-sm opacity-70">
      Ces données sont lues en base PostgreSQL par demo/views.py et rendues ici sans aucun appel API manuel.
    </p>

    <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
      <div v-for="note in notes" :key="note.id" class="card bg-base-100 shadow">
        <div class="card-body">
          <h2 class="card-title">{{ note.titre }}</h2>
          <p>{{ note.contenu }}</p>
          <p class="text-xs opacity-60">{{ formatDate(note.cree_le) }}</p>
        </div>
      </div>
    </div>

    <p v-if="notes.length === 0" class="opacity-70">Aucune note en base pour le moment.</p>
  </AppLayout>
</template>
