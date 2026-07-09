from django.conf import settings
from django.db import models


class Todo(models.Model):
    """CRUD de démonstration — app volontairement isolée et facilement
    supprimable une fois les tests terminés. Pour repartir d'un skeleton
    vierge, voir le README (section "Supprimer le CRUD Todo") : retirer ce
    dossier apps/todos/, sa ligne dans INSTALLED_APPS et dans config/urls.py,
    le dossier frontend/src/pages/todos/, et le lien "Todos" dans Navbar.vue.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="todos"
    )
    titre = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    fait = models.BooleanField(default=False)
    cree_le = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["fait", "-cree_le"]

    def __str__(self):
        return self.titre
