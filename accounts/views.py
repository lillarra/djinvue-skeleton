from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from inertia import render

from config.utils import form_errors, parse_body

from .forms import RegisterForm


def register(request):
    if request.method == "POST":
        form = RegisterForm(parse_body(request))
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("demo-index")
        return render(request, "Auth/Register", props={"errors": form_errors(form)})
    return render(request, "Auth/Register", props={"errors": {}})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=parse_body(request))
        if form.is_valid():
            login(request, form.get_user())
            return redirect("demo-index")
        return render(request, "Auth/Login", props={"errors": form_errors(form)})
    return render(request, "Auth/Login", props={"errors": {}})


@require_POST
def logout_view(request):
    # POST uniquement (jamais GET) : une déconnexion est une action qui
    # modifie l'état, elle doit être protégée par le CSRF comme tout POST.
    logout(request)
    return redirect("demo-index")
