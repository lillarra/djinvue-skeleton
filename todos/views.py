from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST
from inertia import render

from config.utils import form_errors, parse_body

from .forms import TodoForm
from .models import Todo


def _todos_props(request, errors=None):
    # request.user.todos : grâce au related_name="todos" du FK dans le
    # modèle (voir todos/models.py). Chaque utilisateur ne voit que les
    # siens : c'est ce filtrage, pas une vérification côté frontend, qui
    # garantit l'isolation entre comptes.
    todos = request.user.todos.values("id", "titre", "description", "fait", "cree_le")
    return {"todos": list(todos), "errors": errors or {}}


@login_required
def index(request):
    return render(request, "Todos/Index", props=_todos_props(request))


@login_required
def create(request):
    form = TodoForm(parse_body(request))
    if form.is_valid():
        todo = form.save(commit=False)
        todo.user = request.user
        todo.save()
        return redirect("todos-index")
    return render(request, "Todos/Index", props=_todos_props(request, form_errors(form)))


@login_required
def edit(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    if request.method == "POST":
        form = TodoForm(parse_body(request), instance=todo)
        if form.is_valid():
            form.save()
            return redirect("todos-index")
        return render(
            request,
            "Todos/Edit",
            props={"todo": _serialize(todo), "errors": form_errors(form)},
        )
    return render(request, "Todos/Edit", props={"todo": _serialize(todo), "errors": {}})


@login_required
@require_POST
def delete(request, pk):
    get_object_or_404(Todo, pk=pk, user=request.user).delete()
    return redirect("todos-index")


def _serialize(todo):
    return {
        "id": todo.id,
        "titre": todo.titre,
        "description": todo.description,
        "fait": todo.fait,
    }
