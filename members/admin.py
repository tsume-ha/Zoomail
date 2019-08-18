from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import User, TmpMember

@admin.register(User)
class UserAdmin(BaseUserAdmin):
	fieldsets = (
		(None, {'fields': ('email', 'year')}), # changed from google_account
		(('Personal info'), {'fields': ('first_name', 'last_name', 'nickname', 'furigana')}),
		(('Permissions'), {'fields': ('is_superuser', 'is_staff', 'groups')}),
	)
	add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'year') # changed from google_account
        }),
    )
	list_display = ('email', 'first_name', 'last_name', 'year',) # changed from google_account
	list_filter = ('email',) # changed from google_account
	search_fields = ('email',) # changed from google_account
	ordering = ('email',) # changed from google_account
	filter_horizontal = ()

admin.site.register(TmpMember)