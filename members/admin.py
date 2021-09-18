from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from custom_admin.admin import custom_admin_site
from .models import User, TestMail


class SuperuserUserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'year')}),
        (('Personal info'), {'fields': ('receive_email', 'livelog_email', 'last_name', 'first_name', 'nickname', 'furigana')}),
        (('Permissions'), {'fields': ('is_staff', 'groups',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'year')
        }),
    )
    list_display = ('year', 'last_name', 'first_name', 'email', 'receive_email') 
    list_display_links = ('year', 'email')
    list_filter = ('year',)
    search_fields = ('last_name', 'first_name',)
    ordering = ('year', 'furigana',)
    filter_horizontal = ('groups',)


class BasicUserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'year')}),
        (('Personal info'), {'fields': ('receive_email', 'livelog_email', 'last_name', 'first_name', 'nickname', 'furigana')}),
        (('Permissions'), {'fields': ('is_staff', 'groups')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'year')
        }),
    )

    def get_all_groups(self, obj):
        return list(obj.groups.all().values_list('name', flat=True))
    get_all_groups.short_description = '係・役職'
    list_display = ('year', 'get_full_name', 'google_login', 'livelog_login', 'is_staff', 'get_all_groups')
    list_display_links = ('year', 'get_full_name')
    list_filter = ('year',)
    search_fields = ('last_name', 'first_name',)
    ordering = ('year', 'furigana',)
    filter_horizontal = ('groups',)


admin.site.register(User, SuperuserUserAdmin)
custom_admin_site.register(TestMail)
custom_admin_site.register(User, BasicUserAdmin)

