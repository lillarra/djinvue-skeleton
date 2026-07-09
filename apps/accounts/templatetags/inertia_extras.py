from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def script_json(value):
    """Rend le JSON déjà sérialisé par inertia-django (chaîne `page`)
    insérable tel quel dans un `<script type="application/json">`.

    On échappe les "/" en "\\/" — exactement la technique utilisée par
    @inertiajs/vue3 lui-même pour générer ce même genre de balise en SSR
    (voir node_modules/@inertiajs/vue3/dist/index.js, recherche
    "useScriptElementForInitialPage"). Ça empêche toute séquence
    "</script" de clore la balise prématurément, sans jamais casser le
    JSON ("/" n'a aucune signification structurelle en JSON).

    Le filtre `|escape` standard ne convient PAS ici : le contenu d'un
    <script> n'est jamais décodé comme du HTML par le navigateur, donc
    échapper les guillemets en `&quot;` les laisserait tels quels dans le
    texte lu par JSON.parse (qui échouerait).
    """
    return mark_safe(value.replace("/", "\\/"))
