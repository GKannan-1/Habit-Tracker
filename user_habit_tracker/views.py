from django.db.models import QuerySet
from rest_framework import viewsets
from .models import Habit, HabitTrackerUser
from .serializers import HabitSerializer


class HabitViewSet(viewsets.ModelViewSet):  # type: ignore[misc]
    serializer_class = HabitSerializer

    def get_queryset(self) -> QuerySet[Habit]:
        user: HabitTrackerUser = self.request.user.tracker
        return Habit.objects.filter(user=user)

    def perform_create(self, serializer: HabitSerializer) -> None:
        user: HabitTrackerUser = self.request.user.tracker
        serializer.save(user=user)
