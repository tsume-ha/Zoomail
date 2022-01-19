from django.apps import AppConfig


class OtherdocsConfig(AppConfig):
    name = "otherdocs"

    def ready(self):
        from . import signals
