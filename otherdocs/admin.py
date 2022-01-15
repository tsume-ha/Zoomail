import datetime

from django.contrib import admin
from custom_admin.admin import custom_admin_site
from .models import Content


class ContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'index', 'updated_at')
    ordering = ('-index', '-updated_at')

    fields = ("title", "file", "detail", "index", "created_by", "updated_by", "created_at", "updated_at")

    def save_model(self, request, obj, form, change) -> None:
        if not change:
            # created
            obj.created_by = request.user
            obj.created_at = datetime.datetime.now()
            obj.updated_by = request.user
            obj.updated_at = datetime.datetime.now()
        else:
            obj.updated_by = request.user
            obj.updated_at = datetime.datetime.now()
        return super().save_model(request, obj, form, change)


class ContentCustomAdmin(ContentAdmin):
    readonly_fields = ("created_by", "updated_by", "created_at", "updated_at")

admin.site.register(Content, ContentAdmin)
custom_admin_site.register(Content, ContentCustomAdmin)
