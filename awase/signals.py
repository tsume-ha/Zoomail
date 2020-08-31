from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Calendar, CollectHour
import datetime


@receiver(post_save, sender=Calendar)
def Create_Collecthour_from_Calendar(sender, instance, **kwargs):
    calendar = instance
    date = calendar.days_begin
    while date <= calendar.days_end:
        CollectHour.objects.get_or_create(
            calendar = calendar,
            date = date,
            defaults = {'hour_begin': 9, 'hour_end': 24},
            )
        date += datetime.timedelta(days=1)