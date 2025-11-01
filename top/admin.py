from django.contrib import admin

from custom_admin.admin import custom_admin_site
from .models import Announcement

admin.site.register(Announcement)
custom_admin_site.register(Announcement)
