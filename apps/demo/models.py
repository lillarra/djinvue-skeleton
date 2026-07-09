from django.db import models


class Note(models.Model):
    """Modèle de démonstration : prouve que des données lues dans PostgreSQL
    arrivent bien jusqu'au composant Vue de la page d'accueil (voir
    apps/demo/views.py et frontend/src/pages/demo/Index.vue). Modifiable librement
    depuis l'admin Django (/admin) ou `manage.py dbshell` pour voir le
    changement apparaître au rechargement de la page.
    """

    titre = models.CharField(max_length=200)
    contenu = models.TextField()
    cree_le = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-cree_le"]

    def __str__(self):
        return self.titre
