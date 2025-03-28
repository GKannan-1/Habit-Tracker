from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

# Create your views here.


def home_page(request: HttpRequest) -> HttpResponse:
    return render(request, "home.html")


def existing_user(request: HttpRequest) -> HttpResponse:
    return HttpResponse("Fix Soon")


def new_user(request: HttpRequest) -> HttpResponse:
    return HttpResponse("Fix Soon")


def post_submitted_unexpectedly(request: HttpRequest) -> HttpResponse:
    return HttpResponse("Fix Soon")
