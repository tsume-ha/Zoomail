from django.apps import AppConfig


class SoundConfig(AppConfig):
    name = "sound"

    def ready(self):
        from . import signals
