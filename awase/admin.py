from django.contrib import admin
from .models import Calendar, CalendarUser, Schedule, CollectHour

admin.site.register(Calendar)
admin.site.register(CalendarUser)
admin.site.register(Schedule)
admin.site.register(CollectHour)