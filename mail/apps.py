from django.apps import AppConfig


class MailConfig(AppConfig):
    name = "mail"

    def ready(self):
        from . import signals
