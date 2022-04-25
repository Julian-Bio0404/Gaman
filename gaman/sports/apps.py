from django.apps import AppConfig


class SportsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gaman.sports'

    def ready(self) -> None:
        from . import signals
        return super().ready()
