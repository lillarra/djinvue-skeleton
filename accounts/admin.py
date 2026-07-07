from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

from .models import User

# On réutilise tel quel le UserAdmin standard de Django : notre modèle User
# custom a exactement les mêmes champs que celui par défaut.
admin.site.register(User, UserAdmin)
