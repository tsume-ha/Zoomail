from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, TmpMember

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'year')}),
        (('Personal info'), {'fields': ('last_name', 'first_name', 'nickname', 'furigana')}),
        (('Permissions'), {'fields': ('is_superuser', 'is_staff', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'year')
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'year',)
    list_filter = ('email',)
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('groups',)

admin.site.register(TmpMember)