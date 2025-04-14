from rest_framework import serializers
from .models import Habit, HabitTrackerUser
from django_stubs_ext.db.models import TypedModelMeta


class UserSerializer(serializers.ModelSerializer[HabitTrackerUser]):
    username = serializers.CharField(source="author.username", read_only=True)

    class Meta(TypedModelMeta):
        model = HabitTrackerUser
        fields: list[str] = ["id", "username"]


class HabitSerializer(serializers.ModelSerializer[Habit]):
    owner = UserSerializer(read_only=True)

    class Meta(TypedModelMeta):
        model = Habit

        # Data that is exported by serializing object into data
        fields: list[str] = ["id", "title", "text", "created_at", "updated_at", "owner"]

        # Data that is NOT deserialized by deserializing data into objects. So data sent from front-end
        # to back-end will be "title" and "text", it can figure out "id" from the URL, and it can figure
        # out "owner" by checking who is sending the request and finding the associated HabitTrackerUser.
        read_only_fields: list[str] = ["id", "created_at", "updated_at", "owner"]
