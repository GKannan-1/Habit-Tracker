from django.urls import path
from django.urls.resolvers import URLPattern

from . import views

urlpatterns: list[URLPattern] = [
    path("", views.home_page, name="home_page"),
    path("display_list", views.display_list, name="display_list")
]
