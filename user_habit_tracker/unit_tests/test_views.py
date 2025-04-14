"""File that tests the HabitViewSet class of the file views.py"""

from rest_framework.test import APIClient, APITestCase
from rest_framework.response import Response
from django.contrib.auth.models import User
from ..models import Habit


class HabitViewSetTestCase(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user: User = User.objects.create_user(
            username="<USER>", password="<PASSWORD>"
        )
        self.client.force_authenticate(user=self.user)

        self.habit_data: dict[str, str] = {
            "title": "Habit",
            "text": "Do Something Daily",
        }

    def test_create_habit(self) -> None:
        response: Response = self.client.post(
            path="/habits/",
            data=self.habit_data,
            format="json",
        )
