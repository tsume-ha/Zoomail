from django.contrib import admin
from custom_admin.admin import custom_admin_site
from .models import Album


class AlbumAdmin(admin.ModelAdmin):
    fields = ('title', 'url', 'held_at', 'thumbnail', 'created_at', 'created_by')
    readonly_fields = ('created_at', 'created_by')
    list_display = ('title', 'url', 'held_at')
    list_display_links = ('title', 'held_at')


admin.site.register(Album, AlbumAdmin)
custom_admin_site.register(Album, AlbumAdmin)

