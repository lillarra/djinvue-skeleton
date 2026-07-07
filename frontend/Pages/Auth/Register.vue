<script setup>
import { useForm } from "@inertiajs/vue3";
import AppLayout from "../../Layouts/AppLayout.vue";

defineProps({
  errors: { type: Object, default: () => ({}) },
});

const form = useForm({
  username: "",
  email: "",
  password1: "",
  password2: "",
});

function submit() {
  form.post("/register");
}
</script>

<template>
  <AppLayout>
    <div class="card mx-auto max-w-sm bg-base-100 shadow">
      <div class="card-body">
        <h1 class="card-title">Inscription</h1>
        <form class="flex flex-col gap-3" @submit.prevent="submit">
          <label class="form-control">
            <span class="label-text">Nom d'utilisateur</span>
            <input v-model="form.username" type="text" class="input input-bordered w-full" />
            <span v-if="errors.username" class="text-sm text-error">{{ errors.username[0] }}</span>
          </label>
          <label class="form-control">
            <span class="label-text">Email</span>
            <input v-model="form.email" type="email" class="input input-bordered w-full" />
            <span v-if="errors.email" class="text-sm text-error">{{ errors.email[0] }}</span>
          </label>
          <label class="form-control">
            <span class="label-text">Mot de passe</span>
            <input v-model="form.password1" type="password" class="input input-bordered w-full" />
            <span v-if="errors.password1" class="text-sm text-error">{{ errors.password1[0] }}</span>
          </label>
          <label class="form-control">
            <span class="label-text">Confirmation du mot de passe</span>
            <input v-model="form.password2" type="password" class="input input-bordered w-full" />
            <span v-if="errors.password2" class="text-sm text-error">{{ errors.password2[0] }}</span>
          </label>
          <button type="submit" class="btn btn-primary mt-2" :disabled="form.processing">
            S'inscrire
          </button>
        </form>
      </div>
    </div>
  </AppLayout>
</template>
