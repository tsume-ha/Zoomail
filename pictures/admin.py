from django.contrib import admin
from custom_admin.admin import custom_admin_site
from .models import Album


class AlbumAdmin(admin.ModelAdmin):
    fields = ("title", "url", "held_at", "thumbnail", "created_at", "created_by")
    readonly_fields = ("created_at", "created_by")
    list_display = ("title", "url", "held_at")
    list_display_links = ("title", "held_at")

    def save_model(self, request, obj, form, change) -> None:
        if not change:
            obj.created_by = request.user
        return super().save_model(request, obj, form, change)


admin.site.register(Album, AlbumAdmin)
custom_admin_site.register(Album, AlbumAdmin)
