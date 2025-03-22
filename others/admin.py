from django.contrib import admin
from custom_admin.admin import custom_admin_site
from .models import File


class FileAdmin(admin.ModelAdmin):
    fields = (
        "title",
        "original_name",
        "file",
        "thumbnail",
        "description",
        "uploaded_at",
        "upload_user",
    )
    readonly_fields = ("uploaded_at", "thumbnail")
    list_display = ("title", "original_name", "upload_user", "uploaded_at")
    list_display_links = ("title", "original_name")

    def save_model(self, request, obj, form, change):
        if not change:
            obj.upload_user = request.user
        super().save_model(request, obj, form, change)


admin.site.register(File, FileAdmin)
custom_admin_site.register(File, FileAdmin)
