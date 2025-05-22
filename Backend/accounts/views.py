from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.middleware.csrf import get_token
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from user_habit_tracker.models import HabitTrackerUser

from typing import Any


@api_view(["GET"])
@authentication_classes([])
@permission_classes([AllowAny])
def get_csrf(request: Request) -> Response:
    response = Response({"detail": "CSRF cookie set"}, status=status.HTTP_200_OK)
    response["X-CSRFToken"] = get_token(request)  # also adds csrf cookie to response
    return response


@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def login_view(request: Request) -> Response:
    username: Any | None = request.data.get("username")
    password: Any | None = request.data.get("password")

    if username is None or password is None:
        return Response(
            {"error": "Please provide both username and password"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user: User | None = authenticate(username=username, password=password)

    if user is None:
        return Response(
            {"error": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )

    login(request, user)
    return Response({"detail": "Successfully logged in"}, status=status.HTTP_200_OK)


@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def logout_view(request: Request) -> Response:
    logout(request)
    return Response({"detail": "Successfully logged out"}, status=status.HTTP_200_OK)


@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def register_view(request: Request) -> Response:
    username: Any | None = request.data.get("username")
    password: Any | None = request.data.get("password")

    if username is None or password is None:
        return Response(
            {"error": "Please provide both username and password"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {"error": "User already exists"}, status=status.HTTP_400_BAD_REQUEST
        )

    user: User = User.objects.create_user(username=username, password=password)
    HabitTrackerUser.objects.create(author=user)

    login(request, user)
    return Response(
        {"detail": "Successfully registered"}, status=status.HTTP_201_CREATED
    )


class SessionView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request: Request, _format: str | None = None) -> Response:
        return Response({"isAuthenticated": True}, status=status.HTTP_200_OK)


class WhoAmIView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request: Request, _format: str | None = None) -> Response:
        return Response({"username": request.user.username}, status=status.HTTP_200_OK)
