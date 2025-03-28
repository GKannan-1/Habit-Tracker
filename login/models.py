from django.contrib.auth.models import User
from django.db import models
from typing import Any


class MyUserProfile(models.Model):
    user: Any = models.OneToOneField(
        User, on_delete=models.CASCADE)
