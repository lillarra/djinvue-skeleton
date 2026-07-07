from django.urls import path

from . import views

urlpatterns = [
    path("todos", views.index, name="todos-index"),
    path("todos/create", views.create, name="todos-create"),
    path("todos/<int:pk>/edit", views.edit, name="todos-edit"),
    path("todos/<int:pk>/delete", views.delete, name="todos-delete"),
]
