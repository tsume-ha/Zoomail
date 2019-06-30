from django.contrib import admin
from .models import Messages, Message_Year, Message_Attachment, Message_Tag

admin.site.register(Messages)
admin.site.register(Message_Year)
admin.site.register(Message_Attachment)
admin.site.register(Message_Tag)
