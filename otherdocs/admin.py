from django.contrib import admin
from .models import Content


class ContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'index', 'updated_at')
    ordering = ('-index', '-updated_at')

admin.site.register(Content, ContentAdmin)
