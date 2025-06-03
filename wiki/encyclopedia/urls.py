from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>/", views.entry, name="entry"),
    path("search/", views.search, name="search"),
    path("wiki/edit/<str:title>/", views.edit, name="edit"),
    path("create_page", views.create, name="create"),
    path("random", views.random, name="random"),
]
