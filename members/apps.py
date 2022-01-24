from django.apps import AppConfig
from django.db.models.signals import post_migrate


class MembersConfig(AppConfig):
    name = "members"

    def ready(self):
        from .signals import create_default_group

        post_migrate.connect(create_default_group, sender=self)
