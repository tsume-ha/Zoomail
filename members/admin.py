from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
	fieldsets = (
		(None, {'fields': ('google_account', 'year')}),
		('Personal info'), {'fields': ('first_name', 'last_name', 'google_account')}),
		('Permissions', {'fields': ('is_admin', )}),
		)
	search_fields = ('google_account',)
	ordering = ('google_account',)
	filter_horizontal = ()

admin.site.unregister(Group)