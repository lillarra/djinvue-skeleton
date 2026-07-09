<script setup>
// Composant partagé, utilisé par AppLayout.vue sur toutes les pages.
// L'utilisateur courant vient d'une prop PARTAGÉE (voir accounts/middleware.py
// -> inertia.share()), donc disponible ici sans avoir à la repasser
// explicitement depuis chaque vue Django.
import { Link, usePage, router } from "@inertiajs/vue3";
import { computed } from "vue";

const page = usePage();
const user = computed(() => page.props.user);

function logout() {
  router.post("/logout");
}
</script>

<template>
  <div class="navbar bg-base-100 shadow-sm">
    <div class="flex-1">
      <Link href="/" class="btn btn-ghost text-xl">Y Project</Link>
    </div>

    <!-- Menu mobile (dropdown) : visible seulement sous md, pour un rendu
         responsive sans dupliquer les liens. -->
    <div class="dropdown dropdown-end md:hidden">
      <div tabindex="0" role="button" class="btn btn-ghost">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
        </svg>
      </div>
      <ul tabindex="0" class="menu dropdown-content bg-base-100 rounded-box z-10 mt-3 w-52 p-2 shadow">
        <li><Link href="/todos">Todos</Link></li>
        <template v-if="user">
          <li><button @click="logout">Déconnexion ({{ user.username }})</button></li>
        </template>
        <template v-else>
          <li><Link href="/login">Connexion</Link></li>
          <li><Link href="/register">Inscription</Link></li>
        </template>
      </ul>
    </div>

    <!-- Menu desktop -->
    <div class="hidden flex-none gap-2 md:flex">
      <Link href="/todos" class="btn btn-ghost">Todos</Link>
      <template v-if="user">
        <span class="self-center text-sm opacity-70">{{ user.username }}</span>
        <button @click="logout" class="btn btn-ghost">Déconnexion</button>
      </template>
      <template v-else>
        <Link href="/login" class="btn btn-ghost">Connexion</Link>
        <Link href="/register" class="btn btn-primary">Inscription</Link>
      </template>
    </div>
  </div>
</template>
