from django.contrib import admin
from .models import Message, MessageYear, Attachment, Bookmark, To

admin.site.register(Message)
admin.site.register(MessageYear)
admin.site.register(Attachment)
admin.site.register(Bookmark)
admin.site.register(To)
