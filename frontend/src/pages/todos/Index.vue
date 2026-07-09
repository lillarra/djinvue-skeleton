<script setup>
// CRUD de démonstration (voir apps/todos/models.py pour comment le
// supprimer proprement plus tard, y compris ce dossier
// frontend/src/pages/todos/). Page protégée par @login_required côté
// Django : on n'y arrive jamais sans être connecté.
// Si des composants dédiés aux todos sont extraits un jour, les mettre
// dans frontend/src/components/todos/ (miroir de apps/todos).
import { Link, useForm, router } from "@inertiajs/vue3";
import AppLayout from "../../layouts/AppLayout.vue";

defineProps({
  todos: { type: Array, default: () => [] },
  errors: { type: Object, default: () => ({}) },
});

const form = useForm({
  titre: "",
  description: "",
});

function submit() {
  form.post("/todos/create", {
    onSuccess: () => form.reset(),
  });
}

function remove(id) {
  router.post(`/todos/${id}/delete`);
}
</script>

<template>
  <AppLayout>
    <h1 class="mb-6 text-2xl font-bold">Mes todos</h1>

    <form class="card mb-6 bg-base-100 shadow" @submit.prevent="submit">
      <div class="card-body gap-3">
        <label class="form-control">
          <span class="label-text">Titre</span>
          <input v-model="form.titre" type="text" class="input input-bordered w-full" />
          <span v-if="errors.titre" class="text-sm text-error">{{ errors.titre[0] }}</span>
        </label>
        <label class="form-control">
          <span class="label-text">Description (optionnelle)</span>
          <textarea v-model="form.description" class="textarea textarea-bordered w-full"></textarea>
        </label>
        <button type="submit" class="btn btn-primary self-start" :disabled="form.processing">
          Ajouter
        </button>
      </div>
    </form>

    <ul class="flex flex-col gap-2">
      <li
        v-for="todo in todos"
        :key="todo.id"
        class="card bg-base-100 shadow"
      >
        <div
          class="card-body flex-col items-start justify-between gap-3 py-3 sm:flex-row sm:items-center sm:gap-4"
        >
          <div class="min-w-0">
            <p :class="{ 'line-through opacity-50': todo.fait }" class="font-medium break-words">
              {{ todo.titre }}
            </p>
            <p v-if="todo.description" class="text-sm break-words opacity-70">{{ todo.description }}</p>
          </div>
          <div class="flex shrink-0 gap-2">
            <Link :href="`/todos/${todo.id}/edit`" class="btn btn-sm">Éditer</Link>
            <button class="btn btn-sm btn-error" @click="remove(todo.id)">Supprimer</button>
          </div>
        </div>
      </li>
    </ul>

    <p v-if="todos.length === 0" class="opacity-70">Aucun todo pour le moment.</p>
  </AppLayout>
</template>
