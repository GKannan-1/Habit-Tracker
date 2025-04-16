"""File that holds the HabitViewSet Class and its appropriate viewset methods"""

from django.db.models import QuerySet
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import BaseSerializer

from .models import Habit, HabitTrackerUser
from .serializers import HabitSerializer

from typing import cast


class HabitViewSet(viewsets.ModelViewSet[Habit]):
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]
    # self.request.user means the instance of the django User class associated with the request.
    # The request doesn't have the user information in it, but django saves which user is
    # interacting with it since only one user at a time can use a viewset.

    def get_queryset(self) -> QuerySet[Habit]:
        # Django magic, but even though accessing tracker should return a type of
        # OneToOneField[User], at runtime Django links tracker to what its reference is
        # pointing to. So the return time of self.request.user.tracker would be
        # HabitTrackerUser whenever used at runtime, not the OneToOneField[User]
        assert self.request.user.is_authenticated
        owner: HabitTrackerUser = self.request.user.tracker
        return Habit.objects.filter(owner=owner)

    def perform_create(self, serializer: BaseSerializer[Habit]) -> None:
        """
        Helper method that the create method calls when it knows that the data is valid.
        The default is just serializer.save(), but we have to inject the owner data that is only known
        at the time of the request.
        :param serializer: The serializer used to serialize the Habit
        """
        assert self.request.user.is_authenticated
        owner: HabitTrackerUser = self.request.user.tracker
        cast(HabitSerializer, serializer).save(owner=owner)


# TODO: Create view functions for registering users or logging in users (can use separate view file or same), and then adjust the router file accordingly.
