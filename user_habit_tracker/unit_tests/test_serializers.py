"""File that tests the classes UserSerializer and HabitSerializer of the file serializers.py"""

from django.test import TestCase
from django.contrib.auth.models import User
from ..models import HabitTrackerUser, Habit
from ..serializers import UserSerializer, HabitSerializer
from rest_framework.serializers import ModelSerializer
from django.db.models import Model
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from io import BytesIO
from typing import Any, Type, TypeVar

M = TypeVar("M", bound=Model)
S = TypeVar("S", bound=ModelSerializer[Any])


class HabitSerializerTestCase(TestCase):
    def setUp(self) -> None:
        """
        Hook method for setting up the test fixture before exercising it.
        """
        user1: User = User.objects.create_user(
            username="testuser",
            password="password",
        )
        self.habit_tracker_user_1: HabitTrackerUser = HabitTrackerUser.objects.create(
            author=user1
        )

        # habit_tracker_user_1 habits
        user_1_first_habit: Habit = Habit.objects.create(
            title="Exercise",
            text="Do 30 minutes of exercise daily",
            owner=self.habit_tracker_user_1,
        )
        user_1_second_habit: Habit = Habit.objects.create(
            title="Read",
            text="Do 30 minutes of reading daily",
            owner=self.habit_tracker_user_1,
        )

        self.user_1_first_habit_id: int = user_1_first_habit.id
        self.user_1_second_habit_id: int = user_1_second_habit.id

        self.renderer = JSONRenderer()
        self.parser = JSONParser()

    def serialize_data_integrity(self, serializer_class: Type[S], instance: M) -> None:
        """
        Takes in a serializer class and an instance and serializes it, comparing the serializer's data parameter with
        the data parsed from the serializer through the JSON stream, raising an error if the data is different.
        :param serializer_class: Class that serializes the object.
        :param instance: Object that is being serialized.
        :raises AssertionError: Raised if serializer's data is different then expected.
        """
        serializer: S = serializer_class(instance)

        serializer_json_data: bytes = self.renderer.render(serializer.data)
        serializer_json_stream: BytesIO = BytesIO(serializer_json_data)
        serializer_json_parsed_data: Any = self.parser.parse(serializer_json_stream)

        self.assertEqual(serializer.data, serializer_json_parsed_data)

    def test_serializes_user_properly(self) -> None:
        self.serialize_data_integrity(UserSerializer, self.habit_tracker_user_1)

    def test_serializes_habit_properly(self) -> None:
        self.serialize_data_integrity(
            HabitSerializer,
            Habit.objects.get(
                pk=self.user_1_first_habit_id,
            ),
        )

        self.serialize_data_integrity(
            HabitSerializer,
            Habit.objects.get(
                pk=self.user_1_second_habit_id,
            ),
        )

    def test_user_serializer_structure(self) -> None:
        serializer = UserSerializer(self.habit_tracker_user_1)
        serializer_dict: dict[str, Any] = {
            "id": serializer.data["id"],
            "username": serializer.data["username"],
        }

        self.assertDictEqual(serializer.data, serializer_dict)

    def test_habit_serializer_structure(self) -> None:
        serializer = HabitSerializer(Habit.objects.get(pk=self.user_1_first_habit_id))
        serializer_dict: dict[str, Any] = {
            "id": serializer.data["id"],
            "title": serializer.data["title"],
            "text": serializer.data["text"],
            "created_at": serializer.data["created_at"],
            "updated_at": serializer.data["updated_at"],
            "owner": serializer.data["owner"],
        }

        self.assertDictEqual(serializer.data, serializer_dict)
