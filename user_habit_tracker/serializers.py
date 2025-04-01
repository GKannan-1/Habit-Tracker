from rest_framework import serializers
from .models import Habit, HabitTrackerUser
from typing import Any


class HabitSerializer(serializers.ModelSerializer):  # type: ignore[misc]
    class Meta:
        model = Habit
        fields: list[str] = ["id", "title", "text", "created_at", "updated_at"]

    def create(self, validated_data: dict[str, Any]) -> Habit:
        user: HabitTrackerUser = self.context["user"]
        return Habit.objects.create(user=user, **validated_data)

    def update(self, instance: Habit, validated_data: dict[str, Any]) -> Habit:
        instance.title = validated_data.get("title", instance.title)
        instance.text = validated_data.get("text", instance.text)
        instance.save()
        return instance
