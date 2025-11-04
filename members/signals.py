from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group


@receiver(post_save, sender=User)
def update_user_group(sender, instance, created, **kwargs):
    if instance.is_staff:
        group, created = Group.objects.get_or_create(id=1, name="Staff")
        if not instance.groups.filter(id=group.id).exists():
            instance.groups.add(group)
    else:
        if instance.groups.filter(id=1).exists():
            instance.groups.remove(1)
