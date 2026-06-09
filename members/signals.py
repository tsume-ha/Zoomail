from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group


ADMIN_GROUP_NAME = "Zoomail管理者"


@receiver(post_save, sender=get_user_model())
def update_user_group(sender, instance, created, **kwargs):
    group, created = Group.objects.get_or_create(name=ADMIN_GROUP_NAME)
    if instance.is_staff:
        if not instance.groups.filter(id=group.id).exists():
            instance.groups.add(group)
    else:
        if instance.groups.filter(id=group.id).exists():
            instance.groups.remove(group)
