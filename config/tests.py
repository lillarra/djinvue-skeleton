"""Tests de la configuration du projet."""

import ast
import re

import django
import environ
from django.conf import settings
from django.db import connection
from django.test import SimpleTestCase, TestCase

SETTINGS_PATH = settings.BASE_DIR / "config" / "settings.py"
ENV_EXAMPLE_PATH = settings.BASE_DIR / ".env.example"


def read_env_example():
    """Renvoie les variables déclarées dans .env.example, avec leur valeur.

    Les lignes commentées ne comptent pas comme des déclarations.
    """
    content = ENV_EXAMPLE_PATH.read_text(encoding="utf-8")
    return dict(re.findall(r"^([A-Z0-9_]+)=(.*)$", content, re.MULTILINE))


def find_env_calls():
    """Renvoie les appels env(...) et env.xxx(...) écrits dans settings.py.

    L'analyse porte sur l'arbre syntaxique : les commentaires sont ignorés
    et un appel écrit sur plusieurs lignes est reconnu.
    """
    tree = ast.parse(SETTINGS_PATH.read_text(encoding="utf-8"))
    calls = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if isinstance(func, ast.Attribute):
            func = func.value
        if isinstance(func, ast.Name) and func.id == "env":
            calls.append(node)
    return calls


class DjangoVersionTests(SimpleTestCase):
    """Vérifie la version de Django installée."""

    def test_django_version_is_6_1(self):
        # Seules les versions majeure et mineure comptent : les correctifs
        # (6.1.1, 6.1.2, etc.) sont acceptés.
        self.assertEqual(django.VERSION[:2], (6, 1))


class DatabaseConnectionTests(TestCase):
    """Vérifie que la base de données répond."""

    def test_database_is_reachable_and_is_postgresql(self):
        self.assertEqual(connection.vendor, "postgresql")
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            self.assertEqual(cursor.fetchone(), (1,))


class EnvExampleTests(SimpleTestCase):
    """Vérifie que .env.example suffit pour remplir un .env."""

    def test_every_variable_read_by_settings_is_declared(self):
        calls = find_env_calls()
        # Sans cette garde, le test passerait à vide si les réglages ne
        # lisaient plus leurs variables par `env`.
        self.assertTrue(calls, "Aucun appel env(...) trouvé dans settings.py.")

        names = set()
        for call in calls:
            # Le nom doit être écrit en clair en premier argument : sinon le
            # test ne peut pas le relever et doit le signaler.
            first_arg = call.args[0] if call.args else None
            self.assertTrue(
                isinstance(first_arg, ast.Constant)
                and isinstance(first_arg.value, str),
                f"settings.py, ligne {call.lineno} : nom de variable illisible.",
            )
            names.add(first_arg.value)

        missing = sorted(names - read_env_example().keys())
        self.assertEqual(missing, [], "Variables absentes de .env.example.")

    def test_database_url_is_a_valid_postgresql_config(self):
        url = read_env_example().get("DATABASE_URL", "")
        config = environ.Env.db_url_config(url)

        self.assertEqual(config.get("ENGINE"), "django.db.backends.postgresql")
        self.assertTrue(config.get("HOST"), "Hôte absent de DATABASE_URL.")
        self.assertTrue(config.get("NAME"), "Nom de base absent de DATABASE_URL.")
