from django.urls import path

from . import views

urlpatterns = [
    path("", views.home),
    path("sobre/", views.sobre),
    path("contato/", views.contato),
]
