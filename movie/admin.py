from django.contrib import admin
from custom_admin.admin import custom_admin_site
from .models import YoutubeURL


class YoutubeURLAdmin(admin.ModelAdmin):
    fields = ('title', 'url', 'textcontent', 'held_at', 'created_at', 'created_by')
    readonly_fields = ('created_at', 'created_by')
    list_display = ('title', 'url', 'held_at')
    list_display_links = ('title', 'held_at')


admin.site.register(YoutubeURL, YoutubeURLAdmin)
custom_admin_site.register(YoutubeURL, YoutubeURLAdmin)

