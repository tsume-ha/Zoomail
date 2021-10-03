from django.apps import AppConfig


class PicturesConfig(AppConfig):
    name = 'pictures'
    
    def ready(self):
        from . import signals
