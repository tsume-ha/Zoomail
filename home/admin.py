from django.contrib import admin
from .models import Announcement

admin.site.register(Announcement)
from custom_admin.admin import custom_admin_site
custom_admin_site.register(Announcement)