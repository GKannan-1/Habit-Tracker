"""Models registered here can be accessed in the django-admin site.
Just have to create a superuser"""

from django.contrib import admin
from .models import HabitTrackerUser, Habit

# Register your models here.

admin.site.register(HabitTrackerUser)
admin.site.register(Habit)
