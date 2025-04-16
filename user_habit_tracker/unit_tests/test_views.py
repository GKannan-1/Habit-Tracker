"""File that tests the HabitViewSet class of the file views.py"""

from rest_framework.test import APIClient, APITestCase
from rest_framework.response import Response
from django.utils.timezone import localtime
import datetime
from django.contrib.auth.models import User
from ..models import Habit, HabitTrackerUser


class HabitViewSetTestCase(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user: User = User.objects.create_user(
            username="<USER>", password="<PASSWORD>"
        )
        HabitTrackerUser.objects.create(
            author=self.user,
        )
        self.client.force_authenticate(user=self.user)

    def test_create_habit(self) -> None:
        habit_data: dict[str, str] = {
            "title": "Habit",
            "text": "Do Something Daily",
        }
        response: Response = self.client.post(
            path="/habits/",
            data=habit_data,
            format="json",
        )

        # Ensure the request was sent properly and that a proper response was given
        self.assertEqual(response.status_code, 201)

        # Response given has same text and title parameters that was sent out in self.habit_data
        self.assertEqual(response.data["title"], habit_data["title"])
        self.assertEqual(response.data["text"], habit_data["text"])

        # Habit object successfully created by request
        self.assertEqual(Habit.objects.count(), 1)

        # Habit object title, text, and owner parameters are equal to what was sent out in self.habit_data request
        self.assertEqual(Habit.objects.first().title, habit_data["title"])
        self.assertEqual(Habit.objects.first().text, habit_data["text"])
        self.assertEqual(Habit.objects.first().owner.author, self.user)

    def test_list_habits(self) -> None:
        habit: Habit = Habit.objects.create(
            title="Test Habit",
            text="Check it",
            owner=HabitTrackerUser.objects.get(author=self.user),
        )
        response: Response = self.client.get("/habits/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_habit(self) -> None:
        habit: Habit = Habit.objects.create(
            title="Test Habit",
            text="Check it",
            owner=HabitTrackerUser.objects.get(author=self.user),
        )
        response: Response = self.client.get(f"/habits/{habit.id}/")

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data["title"], habit.title)
        self.assertEqual(response.data["text"], habit.text)
        self.assertEqual(
            response.data["owner"]["username"], habit.owner.author.username
        )
        self.assertEqual(response.data["owner"]["id"], habit.owner.author.id)
        self.assertEqual(response.data["id"], habit.id)
        self.assertEqual(
            response.data["created_at"], localtime(habit.created_at).isoformat()
        )
        self.assertEqual(
            response.data["updated_at"], localtime(habit.updated_at).isoformat()
        )
        self.assertLess(
            abs(habit.created_at - habit.updated_at),
            datetime.timedelta(milliseconds=0.5),
        )

    def test_update_habit(self) -> None:
        habit: Habit = Habit.objects.create(
            title="Old Habit",
            text="Update me",
            owner=HabitTrackerUser.objects.get(author=self.user),
        )
        response: Response = self.client.put(
            f"/habits/{habit.id}/",
            data={
                "title": "New Title",
                "text": "Updated Text",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        habit.refresh_from_db()
        self.assertEqual(habit.title, "New Title")
        self.assertEqual(habit.text, "Updated Text")
        self.assertGreater(
            abs(habit.updated_at - habit.created_at),
            datetime.timedelta(milliseconds=0.5),
        )

    def test_delete_habit(self) -> None:
        habit: Habit = Habit.objects.create(
            title="To Delete",
            text="Remove me",
            owner=HabitTrackerUser.objects.get(author=self.user),
        )
        self.assertEqual(Habit.objects.count(), 1)
        response: Response = self.client.delete(f"/habits/{habit.id}/")

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Habit.objects.count(), 0)
