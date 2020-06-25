from django.contrib import admin
from django.urls import path
from . import views


# defing the routes of the pages
urlpatterns = [
    path('update', views.update),
    path('', views.index, name="index"),
    path('recherche', views.research, name="recherche"),
    path('create', views.create_account, name="create"),
    path('logout', views.logout, name="logout"),
    path('connexion', views.connexion, name="connexion"),
    path('index', views.index, name="index"),
    path('profil', views.profil, name="profil"),
    path('details/<int:id>', views.details, name="details"),
]
