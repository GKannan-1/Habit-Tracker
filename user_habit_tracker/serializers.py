from rest_framework import serializers
from .models import Habit, HabitTrackerUser


class UserSerializer(serializers.ModelSerializer):  # type: ignore[misc]
    username = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = HabitTrackerUser
        fields: list[str] = ["id", "username"]


class HabitSerializer(serializers.ModelSerializer):  # type: ignore[misc]
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Habit
        fields: list[str] = ["id", "title", "text",
                             "created_at", "updated_at", "owner"]
