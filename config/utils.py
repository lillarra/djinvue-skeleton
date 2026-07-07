import json


def parse_body(request):
    """Renvoie les données POST envoyées par Inertia.

    Le client Inertia envoie les formulaires en JSON (Content-Type:
    application/json), pas en `application/x-www-form-urlencoded`. Or
    `request.POST` ne sait lire que ce dernier format et resterait vide.
    On utilise cet utilitaire partout où l'on construit un Form Django à
    partir d'une requête Inertia, ex: `RegisterForm(parse_body(request))`.
    """
    if request.content_type == "application/json":
        return json.loads(request.body or "{}")
    return request.POST


def form_errors(form):
    """Convertit les erreurs d'un Form Django en dict de listes de strings,
    directement utilisable comme prop Inertia côté Vue."""
    return {field: [str(e) for e in errs] for field, errs in form.errors.items()}
