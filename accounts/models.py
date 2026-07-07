from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Utilisateur de l'application.

    On part d'un modèle User custom (copie vide de AbstractUser) dès le
    début du projet : c'est une pratique standard Django, car changer de
    modèle User après coup (une fois des migrations appliquées) est très
    pénible. Ici il se comporte exactement comme le User par défaut ; on
    pourra lui ajouter des champs plus tard sans tout casser.
    """

    pass
