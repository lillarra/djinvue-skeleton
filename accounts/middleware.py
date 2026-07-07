from inertia import share


def inertia_share(get_response):
    """Partage l'utilisateur courant à TOUTES les pages Inertia.

    `share()` ajoute des props globales, disponibles dans n'importe quel
    composant Vue via `usePage().props` (voir frontend/Components/Navbar.vue).
    On utilise un lambda pour que la requête `request.user` ne soit évaluée
    que si la prop est effectivement consommée côté client (lazy evaluation).
    """

    def middleware(request):
        share(
            request,
            user=lambda: (
                {"id": request.user.id, "username": request.user.username}
                if request.user.is_authenticated
                else None
            ),
        )
        return get_response(request)

    return middleware
