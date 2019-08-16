from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
	fieldsets = (
		(None, {'fields': ('google_account', 'year')}),
		(('Personal info'), {'fields': ('first_name', 'last_name')}),
		(('Permissions'), {'fields': ('is_superuser', 'is_staff', 'groups')}),
	)
	add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('google_account', 'password1', 'password2', 'year')
        }),
    )
	list_display = ('google_account', 'first_name', 'last_name', 'year',)
	list_filter = ('google_account',)
	search_fields = ('google_account',)
	ordering = ('google_account',)
	filter_horizontal = ()

# admin.site.unregister(Group)