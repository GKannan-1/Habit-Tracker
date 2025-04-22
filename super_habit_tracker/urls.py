"""
URL configuration for super_habit_tracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import include, path
from django.urls.resolvers import URLResolver
from rest_framework.routers import DefaultRouter
from user_habit_tracker.views import HabitViewSet

router = DefaultRouter()
# r prefix tells python to treat backlashes in string as raw characters and not an escape line character
router.register(r"habits", HabitViewSet, basename="habits")

# URLResolver used for include, URLPattern used for explicit mapping to view function
# router generates all default urls for HabitViewSet
urlpatterns: list[URLResolver] = [
    path("", include(router.urls)),
    path("auth/", include("accounts.urls")),
]
