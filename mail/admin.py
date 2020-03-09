from django.contrib import admin
from .models import SendMailAddress, MessageProcess

admin.site.register(SendMailAddress)
admin.site.register(MessageProcess)