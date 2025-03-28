from django.urls import path
from django.urls.resolvers import URLPattern

from . import views

urlpatterns: list[URLPattern] = [
    path("existing_user", views.existing_user, name="existing_user"),
    path("new_user", views.new_user, name="new_user"),
    path("", views.post_submitted_unexpectedly,
         name="post_submitted_unexpectedly")
]
