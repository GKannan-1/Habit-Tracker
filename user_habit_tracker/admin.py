from django.contrib import admin
from .models import HabitTrackerUser, Habit

# Register your models here.


admin.site.register(HabitTrackerUser)
admin.site.register(Habit)
