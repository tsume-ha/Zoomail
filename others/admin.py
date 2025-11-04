from django.contrib import admin
from custom_admin.admin import custom_admin_site
from .models import File
from .forms import FileUploadForm


class FileAdmin(admin.ModelAdmin):
    form = FileUploadForm
    fields = (
        "filename",
        "file",
        "thumbnail",
        "created_at",
        "updated_at",
        "created_by",
        "updated_by",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
        "thumbnail",
        "updated_by",
        "created_by",
    )
    list_display = ("filename", "updated_by", "updated_at")
    list_display_links = ("filename",)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        if form.has_changed():
            obj.updated_by = request.user
        super().save_model(request, obj, form, change)


admin.site.register(File, FileAdmin)
custom_admin_site.register(File, FileAdmin)
