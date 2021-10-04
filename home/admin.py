from django.contrib import admin

from home.views import index
from .models import Announcement, NewContent

admin.site.register(Announcement)
from custom_admin.admin import custom_admin_site
custom_admin_site.register(Announcement)

class NewContentAdmin(admin.ModelAdmin):
    fields = ("index", "genre", "title", "path", "date")
    readonly_fields = ("index", "genre", "title", "path", "date")
    
    list_display = ("index", "genre", "title", "path", "date")
    list_display_links = ("index", "genre", "title", "date")
    
    def get_ordering(self, request):
        return ['index']

admin.site.register(NewContent, NewContentAdmin)

