"""Tests de la configuration du projet."""

import django
from django.test import SimpleTestCase


class DjangoVersionTests(SimpleTestCase):
    """Vérifie la version de Django installée."""

    def test_django_version_is_6_1(self):
        # Seules les versions majeure et mineure comptent : les correctifs
        # (6.1.1, 6.1.2, etc.) sont acceptés.
        self.assertEqual(django.VERSION[:2], (6, 1))
