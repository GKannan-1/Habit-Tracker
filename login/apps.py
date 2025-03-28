from django.apps import AppConfig


class LoginConfig(AppConfig):
    default_auto_field: str = "django.db.models.BigAutoField"
    name: str = "login"

    def ready(self):
        import login.signals  # type: ignore
