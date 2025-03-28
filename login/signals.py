from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models import Model
from login.models import MyUserProfile
from typing import Any


@receiver(post_save, sender=User)
def create_user_profile(sender: type[Model], instance: User, created: bool, **kwargs: Any) -> None:
    if created:
        MyUserProfile.objects.create(user=instance)
