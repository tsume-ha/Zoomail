from django.apps import AppConfig


class AwaseConfig(AppConfig):
    name = 'awase'

    def ready(self):
        from . import signals