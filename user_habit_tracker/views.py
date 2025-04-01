from django.db.models import QuerySet
from rest_framework import viewsets
from .models import Habit, HabitTrackerUser
from .serializers import HabitSerializer


class HabitViewSet(viewsets.ModelViewSet):  # type: ignore[misc]
    # Using none because we need get_query to work with our setup and the OneToOneField,
    # and using all could result in conflicts as well as just not working.
    queryset: QuerySet[Habit] = Habit.objects.none()
    serializer_class = HabitSerializer
    # self.request.user means the instance of the django User class associated with the request
    # The request doesn't have the user information in it, but django saves which user is
    # interacting with it since only one user at a time can use a viewset.

    def get_queryset(self) -> QuerySet[Habit]:
        # Django magic, but even though accessing tracker should return a type of
        # OneToOneField[User], at runtime Django links tracker to what its reference is
        # pointing to. So the return time of self.request.user.tracker would be
        # HabitTrackerUser whenever used at runtime, not the OneToOneField[User]
        owner: HabitTrackerUser = self.request.user.tracker
        return Habit.objects.filter(owner=owner)

    def perform_create(self, serializer: HabitSerializer) -> None:
        owner: HabitTrackerUser = self.request.user.tracker
        serializer.save(owner=owner)
