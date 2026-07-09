<script setup>
import { useForm } from "@inertiajs/vue3";
import AppLayout from "../../layouts/AppLayout.vue";

defineProps({
  errors: { type: Object, default: () => ({}) },
});

const form = useForm({
  username: "",
  password: "",
});

function submit() {
  form.post("/login");
}
</script>

<template>
  <AppLayout>
    <div class="card mx-auto max-w-sm bg-base-100 shadow">
      <div class="card-body">
        <h1 class="card-title">Connexion</h1>
        <form class="flex flex-col gap-3" @submit.prevent="submit">
          <label class="form-control">
            <span class="label-text">Nom d'utilisateur</span>
            <input v-model="form.username" type="text" class="input input-bordered w-full" />
            <span v-if="errors.username" class="text-sm text-error">{{ errors.username[0] }}</span>
          </label>
          <label class="form-control">
            <span class="label-text">Mot de passe</span>
            <input v-model="form.password" type="password" class="input input-bordered w-full" />
          </label>
          <span v-if="errors.__all__" class="text-sm text-error">{{ errors.__all__[0] }}</span>
          <button type="submit" class="btn btn-primary mt-2" :disabled="form.processing">
            Se connecter
          </button>
        </form>
      </div>
    </div>
  </AppLayout>
</template>
