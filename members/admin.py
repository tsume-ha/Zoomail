from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, TmpMember

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'year')}),
        (('Personal info'), {'fields': ('receive_email', 'last_name', 'first_name', 'nickname', 'furigana')}),
        (('Permissions'), {'fields': ('is_staff', 'groups', 'user_permissions')}),
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
    filter_horizontal = ('groups', 'user_permissions')

admin.site.register(TmpMember)