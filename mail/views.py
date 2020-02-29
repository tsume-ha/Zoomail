from django.shortcuts import render
from members.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

def index(request):
    pass


@receiver(post_save, sender=User)
def signalmethod(sender, **kwargs):
	print('done')