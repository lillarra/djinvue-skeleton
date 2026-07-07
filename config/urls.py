"""
Routes du projet. Chaque app Django déclare ses propres URLs dans son
fichier urls.py ; on les inclut ici. C'est ce qui permet de supprimer
proprement l'app todos plus tard : il suffira de retirer la ligne
correspondante ci-dessous (voir le README, section "Suppression du CRUD Todo").
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("accounts.urls")),
    path("", include("demo.urls")),
    # CRUD Todo, supprimable : voir todos/models.py et le README.
    path("", include("todos.urls")),
]
