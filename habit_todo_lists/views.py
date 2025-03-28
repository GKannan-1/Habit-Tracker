from django.http import HttpResponse, HttpRequest
from django.shortcuts import render


def home_page(request: HttpRequest) -> HttpResponse:
    return render(request, "habit_todo_lists/home.html")


def display_list(request: HttpRequest) -> HttpResponse:
    return render(request, "habit_todo_lists/list.html", {"item": request.POST.get("item_text")})
