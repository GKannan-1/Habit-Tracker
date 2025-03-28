from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from .types import HasID, cast

# Create your views here.


def home_page(request: HttpRequest) -> HttpResponse:
    user: User = User.objects.create_user(username="pizza", password="pie")
    typed_user: HasID = cast(HasID, user)
    user_id: int = typed_user.id
    return render(request, "home.html")
