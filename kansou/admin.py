from django.contrib import admin
from custom_admin.admin import custom_admin_site
from .models import Kansouyoushi


class KansouAdmin(admin.ModelAdmin):
    fields = ('live', 'numbering', 'detail', 'file', 'performed_at', 'created_at', 'created_by')
    readonly_fields = ('created_at', 'created_by')
    list_display = ('live', 'numbering', 'performed_at')
    list_display_links = ('live', 'numbering', 'performed_at')


admin.site.register(Kansouyoushi, KansouAdmin)
custom_admin_site.register(Kansouyoushi, KansouAdmin)
