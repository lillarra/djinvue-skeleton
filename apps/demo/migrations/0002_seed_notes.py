# Migration de données : insère quelques exemples pour que la page démo
# affiche immédiatement du contenu venant de PostgreSQL après un `migrate`.
from django.db import migrations

NOTES = [
    {
        "titre": "Bienvenue sur le skeleton",
        "contenu": "Cette note est lue depuis PostgreSQL et affichée par un composant Vue.",
    },
    {
        "titre": "Django + Inertia + Vue",
        "contenu": "Aucun appel API JSON manuel : la vue Django passe les props directement au composant.",
    },
    {
        "titre": "À toi de jouer",
        "contenu": "Modifie ces notes depuis /admin ou `manage.py dbshell` pour voir le changement au rechargement.",
    },
]


def seed_notes(apps, schema_editor):
    Note = apps.get_model("demo", "Note")
    Note.objects.bulk_create(Note(**data) for data in NOTES)


def remove_notes(apps, schema_editor):
    Note = apps.get_model("demo", "Note")
    Note.objects.filter(titre__in=[n["titre"] for n in NOTES]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("demo", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_notes, remove_notes),
    ]
