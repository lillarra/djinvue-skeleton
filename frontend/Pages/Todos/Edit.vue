<script setup>
import { Link, useForm } from "@inertiajs/vue3";
import AppLayout from "../../Layouts/AppLayout.vue";

const props = defineProps({
  todo: { type: Object, required: true },
  errors: { type: Object, default: () => ({}) },
});

const form = useForm({
  titre: props.todo.titre,
  description: props.todo.description,
  fait: props.todo.fait,
});

function submit() {
  form.post(`/todos/${props.todo.id}/edit`);
}
</script>

<template>
  <AppLayout>
    <div class="card mx-auto max-w-lg bg-base-100 shadow">
      <div class="card-body gap-3">
        <h1 class="card-title">Éditer le todo</h1>
        <form class="flex flex-col gap-3" @submit.prevent="submit">
          <label class="form-control">
            <span class="label-text">Titre</span>
            <input v-model="form.titre" type="text" class="input input-bordered w-full" />
            <span v-if="errors.titre" class="text-sm text-error">{{ errors.titre[0] }}</span>
          </label>
          <label class="form-control">
            <span class="label-text">Description</span>
            <textarea v-model="form.description" class="textarea textarea-bordered w-full"></textarea>
          </label>
          <label class="label cursor-pointer justify-start gap-3">
            <input v-model="form.fait" type="checkbox" class="checkbox" />
            <span class="label-text">Fait</span>
          </label>
          <div class="mt-2 flex gap-2">
            <button type="submit" class="btn btn-primary" :disabled="form.processing">
              Enregistrer
            </button>
            <Link href="/todos" class="btn">Annuler</Link>
          </div>
        </form>
      </div>
    </div>
  </AppLayout>
</template>
