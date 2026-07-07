# Y Project — squelette Django + Inertia + Vue 3

Squelette de démarrage pour une stack **Django + Inertia.js + Vue 3 (Composition API) + Vite +
Tailwind CSS + DaisyUI + PostgreSQL**, sans SSR. Pensé pour être réutilisé comme base de départ
sur de futurs projets : code commenté en français, dépendances minimales, toute la config
sensible/variable passe par des variables d'environnement.

## Stack

- **Backend** : Django 5.2 LTS, gestion des dépendances avec [uv](https://docs.astral.sh/uv/)
- **Pont front/back** : [Inertia.js](https://inertiajs.com/) (`inertia-django` côté serveur,
  `@inertiajs/vue3` côté client)
- **Frontend** : Vue 3 (Composition API, JavaScript, pas de TypeScript)
- **Build** : Vite
- **Styles** : Tailwind CSS v4 (CSS-first) + DaisyUI v5
- **Base de données** : PostgreSQL

## Prérequis

- [uv](https://docs.astral.sh/uv/getting-started/installation/) installé
- Node.js + npm
- PostgreSQL accessible (en local via Laragon, Postgres.app, etc.)

## Installation

```bash
# 1. Dépendances Python (crée le .venv automatiquement)
uv sync

# 2. Dépendances JS
npm install

# 3. Config d'environnement
cp .env.example .env
# Éditer .env : générer une SECRET_KEY et renseigner DATABASE_URL, par exemple :
uv run python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# 4. Créer la base PostgreSQL (adapter selon votre installation)
psql -U postgres -h localhost -p 5432 -c "CREATE DATABASE yproject;"

# 5. Appliquer les migrations (crée aussi les 3 notes de démo, voir demo/migrations/0002_seed_notes.py)
uv run manage.py migrate

# 6. (optionnel) Créer un compte admin pour /admin
uv run manage.py createsuperuser
```

## Lancer en développement

Deux process à lancer en parallèle (deux terminaux) :

```bash
uv run manage.py runserver 8500
```

```bash
npm run dev
```

Puis ouvrir **http://localhost:8500**. Vite tourne sur le port 5173 (hot reload) mais ce n'est pas
lui qu'on visite : Django sert les pages et charge les assets Vite via `django-vite`.

## Build de production

```bash
npm run build              # build les assets dans static/dist/
uv run manage.py collectstatic --noinput
```

Avec `DJANGO_DEBUG=False` dans `.env`, django-vite bascule automatiquement en lecture du
`manifest.json` généré par Vite au lieu de pointer vers le serveur de dev.

## Structure du projet

```
config/            réglages Django, urls racine
accounts/           authentification native Django + partage de l'utilisateur courant (Inertia)
demo/                page publique de démonstration (lit des données PostgreSQL)
todos/               CRUD de démonstration, protégé par authentification (voir plus bas)
templates/base.html  layout HTML racine (INERTIA_LAYOUT)
frontend/            code source JS/Vue (Pages, Layouts, Components, entry.js, css)
static/dist/         build Vite (généré, ignoré par git)
```

## Pièges connus (à lire avant de faire évoluer ce skeleton)

- **`@inertiajs/vue3` v3 + `inertia-django` : incompatibilité de protocole, comblée par une
  surcharge de template.** La v3 du client JS a supprimé la lecture de l'ancien format
  `<div id="app" data-page="...">` au profit d'une balise `<script data-page="app"
  type="application/json">` dédiée (protocole v2/v3) — sans fallback. Or `inertia-django` (dernière
  version publiée, et même sa PR de support v3 en cours : voir
  [inertiajs/inertia-django#99](https://github.com/inertiajs/inertia-django/issues/99) et
  [#100](https://github.com/inertiajs/inertia-django/pull/100)) ne génère toujours que l'ancien
  format. Sans correctif, l'app ne se monte jamais (page blanche, `Cannot read properties of null
  (reading 'component')`).

  **Solution appliquée ici** : on surcharge le template `inertia.html` fourni par le paquet
  `inertia` (Django cherche d'abord dans notre propre dossier `templates/`, déclaré dans `DIRS`,
  avant celui du package via `APP_DIRS` — voir `TEMPLATES` dans `config/settings.py`).
  - `templates/inertia.html` : génère la nouvelle balise `<script>` au lieu de l'attribut `data-page`.
  - `accounts/templatetags/inertia_extras.py` : filtre `script_json` qui échappe les `/` en `\/`
    dans le JSON avant de l'insérer dans le `<script>` — exactement la technique utilisée par
    `@inertiajs/vue3` lui-même pour son propre rendu SSR (voir
    `node_modules/@inertiajs/vue3/dist/index.js`, recherche `useScriptElementForInitialPage`).
    Le filtre `|escape` standard de Django ne convient pas ici : le contenu d'un `<script>` n'est
    jamais décodé comme du HTML, donc échapper les guillemets en `&quot;` casserait le JSON.

  À surveiller : si une future version d'`inertia-django` génère nativement ce format (vérifier son
  fichier `inertia/templates/inertia.html` en amont), notre surcharge devient redondante et peut
  être supprimée (avec le filtre `script_json`).
  Important : après avoir ajouté/modifié un module `templatetags`, un redémarrage **complet** du
  serveur Django est nécessaire — l'autoreload de `runserver` ne le détecte pas toujours.
- **Les formulaires Inertia envoient du JSON**, pas du `application/x-www-form-urlencoded` :
  `request.POST` reste vide. D'où l'utilitaire `config/utils.py::parse_body(request)`, utilisé
  partout où l'on construit un `Form` Django à partir d'une requête (voir `accounts/views.py`,
  `todos/views.py`).
- **CSRF** : `CSRF_COOKIE_NAME`/`CSRF_HEADER_NAME` sont alignés dans `config/settings.py` sur ce
  qu'attend le client Inertia (convention Laravel `XSRF-TOKEN` / `X-XSRF-TOKEN`), pour éviter
  d'avoir à configurer quoi que ce soit côté JS.
- **Commentaires Django multi-lignes** : le tag `{# ... #}` ne supporte **pas** plusieurs lignes
  (il n'est alors pas du tout traité comme un commentaire et s'affiche tel quel dans le HTML rendu).
  Utiliser `{% comment %}...{% endcomment %}` pour tout commentaire de template sur plusieurs
  lignes (voir `templates/base.html`).
- **CORS sur les assets Vite en dev** : la page est servie par Django (`:8500`) mais charge des
  scripts `type="module"` depuis Vite (`:5173`) — une origine différente. Un script module
  cross-origin est chargé en mode CORS par le navigateur ; sans `server.cors: true` dans
  `vite.config.js`, il est bloqué silencieusement (page blanche, aucune erreur réseau visible sans
  ouvrir la console).

## Réutiliser ce skeleton / repartir de zéro

Le CRUD Todo (`todos/`) n'existe que pour prouver que l'authentification + CRUD + isolation par
utilisateur fonctionnent. Pour repartir d'un skeleton vierge, supprimer :

1. Le dossier `todos/`
2. Le dossier `frontend/Pages/Todos/`
3. `"todos"` dans `INSTALLED_APPS` (`config/settings.py`)
4. La ligne `path("", include("todos.urls"))` dans `config/urls.py`
5. Le lien "Todos" dans `frontend/Components/Navbar.vue`
6. Une fois `todos` supprimée, `config/utils.py::form_errors` reste utilisé par `accounts` — rien
   à faire de ce côté.

La page démo (`demo/`) et l'authentification (`accounts/`) sont le socle du skeleton : à garder
(et personnaliser) pour un nouveau projet.
