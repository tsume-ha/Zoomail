from django.contrib import admin
from django.contrib.admin import filters
from .models import SendMailAddress, MessageProcess


class MessageProcessAdmin(admin.ModelAdmin):
    list_display = ("message", "Requested", "Processed", "Delivered", "Opened", "Error_occurd")
    list_filter = ["Error_occurd"]


admin.site.register(SendMailAddress)
admin.site.register(MessageProcess, MessageProcessAdmin)
