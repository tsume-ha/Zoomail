from django.contrib import admin
from .models import SendMailAddress, MailLog


class MailLogAdmin(admin.ModelAdmin):
    list_display = ("message", "mail_id", "user", "send_server", "status", "error")
    list_filter = ["status"]


admin.site.register(SendMailAddress)
admin.site.register(MailLog, MailLogAdmin)
