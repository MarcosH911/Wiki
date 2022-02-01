from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("searchEntry", views.searchEntry, name="searchEntry"),
    path("randomEntry", views.randomEntry, name="randomEntry"),
    path("newEntry", views.newEntry, name="newEntry"),
    path("wiki/<str:title>/edit", views.editEntry, name="newEntry")
]
