from django.apps import AppConfig


class KansouConfig(AppConfig):
    name = "kansou"
    
    def ready(self):
        from . import signals
