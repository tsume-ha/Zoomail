from django.contrib import admin
from .models import Announcement, NewContent

admin.site.register(Announcement)
admin.site.register(NewContent)
from custom_admin.admin import custom_admin_site
custom_admin_site.register(Announcement)