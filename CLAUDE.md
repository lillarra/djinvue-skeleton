# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A reusable starter skeleton for a **Django 5.2 LTS + Inertia.js + Vue 3** stack (no SSR): Django serves
pages via `inertia-django`, Vue 3 (Composition API, JS only, no TypeScript) renders them, Vite
handles the frontend build, styling is Tailwind v4 (CSS-first) + DaisyUI v5, PostgreSQL is the
database. Config is 100% env-driven via `django-environ` (see `.env.example`) so it's trivial
to Dockerize later.

The `todos` app (backend `apps/todos/` + frontend `frontend/src/pages/todos/`) is a disposable
demo CRUD proving auth + per-user isolation work — it's meant to be deleted wholesale when reusing
this skeleton for a real project (see README's "Réutiliser ce skeleton" section for the exact
removal checklist). `apps/demo/` and `apps/accounts/` are the permanent skeleton core.

## Conventions

- **Language**: all comments and documentation (docstrings, README, .env.example) are in French.
  Code itself stays in English — variable/function names, database columns, model field names,
  and Django identifiers are all English. French is for prose written for humans, not identifiers.
- **Line endings**: LF (never CRLF) for all text files. The root `.gitattributes` enforces and
  guarantees this normalization on every machine.

## Commands

```bash
uv sync                        # install Python deps (creates .venv)
npm install                    # install JS deps

uv run manage.py runserver 8500   # Django dev server — NOTE: port 8500, not the 8000 default
npm run dev                       # Vite dev server on :5173 (HMR) — run both in parallel

npm run build                     # build frontend into frontend/dist/
uv run manage.py collectstatic --noinput
uv run manage.py migrate
uv run manage.py makemigrations <app_label>   # e.g. accounts, demo, todos (not apps.accounts)
uv run manage.py check
uv run manage.py test             # Django's test runner (no tests written yet — boilerplate only)
```

Visit `http://localhost:8500` (not 5173 — Django serves the pages and pulls Vite assets via
django-vite). Toggle `DJANGO_DEBUG` in `.env` to switch django-vite between dev-server mode and
reading the built `manifest.json`.

**After adding/moving a `templatetags` module or renaming a Django app's dotted path, fully
restart `manage.py runserver`** — `runserver`'s autoreload does not reliably pick this up.

## Architecture

### Directory layout is a 3-way split, not the Django default flat layout

```
config/     Django project only (settings, urls, wsgi/asgi, config/templates/, config/utils.py)
apps/       all business Django apps: apps/accounts, apps/demo, apps/todos
frontend/   all JS/Vue, including its own build output (frontend/dist/)
```

Apps live under `apps.<name>` as their Python dotted path (`INSTALLED_APPS`, `apps.py`'s
`name = "apps.accounts"`, `include("apps.accounts.urls")` in `config/urls.py`), but Django's
**app_label stays the bare name** (`"accounts"`, `"demo"`, `"todos"`) since the label defaults to
the last dotted segment. This is why `AUTH_USER_MODEL = "accounts.User"` (not `"apps.accounts.User"`)
and migration deps use bare labels — don't "fix" these to add the `apps.` prefix.

### Frontend mirrors Django apps by naming convention — this is load-bearing, not cosmetic

`frontend/src/pages/<domain>/` folders (`accounts/`, `demo/`, `todos/`, lowercase) must match the
Inertia component-name strings Django views pass to `render()`/`@inertia()` (e.g.
`apps/accounts/views.py` calls `render(request, "accounts/Login", ...)`). `frontend/src/entry.js`'s
`createInertiaApp({ resolve })` does `import.meta.glob("./pages/**/*.vue")` and looks up
`` `./pages/${name}.vue` `` — renaming a Django app or moving a `.vue` page requires updating
**both sides in lockstep**: the component-name string in the Django view and the file's path under
`pages/`. `frontend/src/components/shared/` holds cross-cutting components (`Navbar.vue`);
domain-specific components would go in `frontend/src/components/<domain>/` (none exist yet).

### Inertia protocol compatibility patch (config/templates/inertia.html)

`inertia-django` (the Python adapter) only ever renders the old `<div id="app" data-page="...">`
bootstrap format. `@inertiajs/vue3` v3 (used here) dropped support for that format entirely and
only reads a `<script data-page="app" type="application/json">` tag. `config/templates/inertia.html`
overrides the package's own template (Django's `TEMPLATES["DIRS"]` — pointing at
`config/templates/`— is checked before the package's `APP_DIRS` template) to emit the new format,
using `apps/accounts/templatetags/inertia_extras.py`'s `script_json` filter to safely escape `/` as
`\/` in the embedded JSON (the same technique `@inertiajs/vue3` itself uses for SSR). If a future
`inertia-django` release generates the new format natively, this override + filter become
redundant. Full details and sources: README's "Pièges connus" section.

### Inertia forms send JSON, not urlencoded

`request.POST` is empty for Inertia form submissions (they're JSON, not
`application/x-www-form-urlencoded`). Every view that builds a Django `Form` from a request uses
`config/utils.py::parse_body(request)` instead of `request.POST`. Validation errors are serialized
via `config/utils.py::form_errors(form)` into `{field: [messages]}` and passed as an Inertia prop
(not the CSRF-style flash/session error bag Laravel's adapter uses).

### CSRF is remapped to Inertia/axios conventions

`config/settings.py` sets `CSRF_COOKIE_NAME = "XSRF-TOKEN"` and
`CSRF_HEADER_NAME = "HTTP_X_XSRF_TOKEN"` so the Inertia client's default cookie/header handling
works without any custom JS — don't rename these without checking that pairing.

### Per-user data isolation pattern (apps/todos)

Views never trust a client-supplied user id; they filter through `request.user.todos` (the
`related_name` on the FK in `apps/todos/models.py`) and use `get_object_or_404(Todo, pk=pk,
user=request.user)` for edit/delete, so a 404 (not a 403) is what a cross-user access attempt gets.
The shared current-user prop (available on every page via `usePage().props.user`) is set once in
`apps/accounts/middleware.py` via `inertia.share()`, not per-view.
