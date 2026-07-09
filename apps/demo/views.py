from inertia import inertia

from .models import Note


@inertia("demo/Index")
def index(request):
    # .values(...) plutôt que de passer le QuerySet tel quel : ça donne un
    # contrôle explicite sur les champs envoyés au frontend (le "id" est
    # notamment exclu par défaut par la sérialisation automatique
    # d'inertia-django, ce qui casserait le `:key` côté Vue).
    notes = Note.objects.values("id", "titre", "contenu", "cree_le")
    return {"notes": list(notes)}
