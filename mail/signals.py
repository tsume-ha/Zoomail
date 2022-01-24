from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import SendMailAddress
from members.models import User
from django.core.exceptions import ObjectDoesNotExist


@receiver(post_save, sender=User)
def update_send_mail_address(sender, instance, **kwargs):
    if instance.send_mail:
        SendMailAddress.objects.update_or_create(
            user=instance,
            year=instance.year,
            defaults={"email": instance.get_receive_email()},
        )

    else:
        try:
            content = SendMailAddress.objects.get(user=instance)
            content.delete()
        except ObjectDoesNotExist:
            pass
