"""
Réglages Django du projet.

Toute valeur sensible ou qui varie selon l'environnement (secret key, mode
debug, hôtes autorisés, connexion base de données...) est lue depuis un
fichier .env via django-environ, jamais codée en dur ici. Cela permet de
garder un seul et même fichier settings.py entre le dev local (Laragon),
un futur environnement Docker ou un serveur de prod : seul le .env change.

Voir .env.example à la racine du projet pour la liste des variables
attendues et leur documentation.
"""

from pathlib import Path

import environ

# BASE_DIR pointe vers la racine du repo (dossier contenant manage.py).
BASE_DIR = Path(__file__).resolve().parent.parent

# Déclaration des variables d'environnement attendues, avec leur type
# Python et une valeur par défaut (utilisée seulement si absente du .env).
# Sans valeur par défaut, environ lève une erreur explicite si la
# variable manque : on préfère un crash clair au démarrage plutôt
# qu'un mauvais comportement silencieux en prod.
env = environ.Env(
    DJANGO_DEBUG=(bool, False),
)

# Lit le fichier .env s'il existe (absent en prod, où les variables sont
# généralement injectées directement par l'environnement d'exécution).
environ.Env.read_env(BASE_DIR / ".env")

SECRET_KEY = env("DJANGO_SECRET_KEY")
DEBUG = env("DJANGO_DEBUG")
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=[])


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Librairies tierces
    "django_vite",
    "inertia",
    # Apps du projet
    "accounts",
    "demo",
    "todos",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    # Partage l'utilisateur courant à toutes les pages Inertia (voir
    # accounts/middleware.py) : doit passer après AuthenticationMiddleware
    # pour avoir accès à request.user.
    "accounts.middleware.inertia_share",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "inertia.middleware.InertiaMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Modèle utilisateur custom (voir accounts/models.py) : à définir avant la
# toute première migration, car il est quasi impossible à changer après.
AUTH_USER_MODEL = "accounts.User"


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases
# DATABASE_URL suit le format standard 12-factor :
#   postgres://USER:PASSWORD@HOST:PORT/NOM_DE_LA_BASE
# ce qui rend la config triviale à reprendre telle quelle dans un futur
# docker-compose.yml (il suffira de changer HOST par le nom du service).
DATABASES = {
    "default": env.db("DATABASE_URL"),
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "fr-fr"

TIME_ZONE = "Europe/Paris"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = "static/"

# static/dist est le dossier de build de Vite (voir vite.config.js) : c'est
# là que collectstatic ira chercher les assets buildés en prod.
STATICFILES_DIRS = [BASE_DIR / "static" / "dist"]

# Dossier où `collectstatic` rassemble tous les fichiers statiques pour la
# prod (assets buildés par Vite inclus). Reste vide en dev.
STATIC_ROOT = BASE_DIR / "staticfiles"

# Après connexion / déconnexion, redirige vers la page d'accueil (page démo).
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"
LOGIN_URL = "/login"

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# --- CSRF : alignement sur les noms attendus par le client Inertia --------
# Le client JS d'Inertia lit le cookie CSRF et le renvoie via un header,
# mais avec les noms utilisés par défaut côté Laravel (XSRF-TOKEN /
# X-XSRF-TOKEN). On aligne Django dessus plutôt que d'ajouter du code JS
# custom : c'est l'option recommandée par la doc d'inertia-django.
CSRF_COOKIE_NAME = "XSRF-TOKEN"
CSRF_HEADER_NAME = "HTTP_X_XSRF_TOKEN"


# --- Configuration django-vite (pont entre Django et le build Vite) -------
# En dev : DJANGO_VITE["default"]["dev_mode"] = True fait pointer les tags
# {% vite_asset %} vers le serveur de dev Vite (localhost:5173, avec HMR).
# En prod : il lit static/dist/manifest.json généré par `npm run build`
# pour connaître les noms de fichiers hashés à injecter.
DJANGO_VITE = {
    "default": {
        "dev_mode": DEBUG,
        "manifest_path": BASE_DIR / "static" / "dist" / ".vite" / "manifest.json",
    }
}

# Layout HTML racine utilisé par inertia-django pour chaque réponse rendue
# côté navigateur (première visite / rechargement complet).
INERTIA_LAYOUT = "base.html"
