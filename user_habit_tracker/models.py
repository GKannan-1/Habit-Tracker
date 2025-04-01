from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class HabitTrackerUser(models.Model):
    author = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="tracker")

    def __str__(self) -> str:
        return f"{self.author.username}'s Tracker"


class Habit(models.Model):
    title = models.CharField(default="", max_length=200)
    text = models.TextField(default="")
    user = models.ForeignKey(
        HabitTrackerUser, default=None, on_delete=models.CASCADE,)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Habit: {self.title}"
