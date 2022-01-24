from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import messages
from social_django.models import UserSocialAuth
from custom_admin.admin import custom_admin_site
from .models import User, TestMail
from .forms import RegisterForm


class SuperuserUserAdmin(BaseUserAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "year",
                    ("last_name", "first_name"),
                    "nickname",
                    "furigana",
                    "email",
                    "livelog_email",
                    "receive_email",
                )
            },
        ),
        (("Permissions"), {"fields": ("is_staff", "is_superuser", "groups")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", ("last_name", "first_name"), "year", "furigana"),
            },
        ),
    )

    def get_all_groups(self, obj):
        return list(obj.groups.all().values_list("name", flat=True))

    get_all_groups.short_description = "係・役職"

    def google_oauth(self, obj):
        try:
            content = UserSocialAuth.objects.get(user=obj, provider="google-oauth2")
            return content.uid
        except:
            return ""

    def livelog_oauth(self, obj):
        try:
            content = UserSocialAuth.objects.get(user=obj, provider="auth0")
            return content.uid
        except:
            return ""

    list_display = (
        "year",
        "get_full_name",
        "google_oauth",
        "livelog_oauth",
        "is_staff",
        "is_superuser",
        "get_all_groups",
        "send_mail",
    )
    list_display_links = ("year", "get_full_name")
    list_filter = ("year", "is_staff", "is_superuser", "send_mail")
    search_fields = (
        "last_name",
        "first_name",
    )
    ordering = (
        "year",
        "furigana",
    )
    filter_horizontal = ("groups",)
    add_form = RegisterForm


class BasicUserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("year", ("last_name", "first_name"), "nickname", "furigana")}),
        (("Permissions"), {"fields": ("is_staff", "groups")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", ("last_name", "first_name"), "year", "furigana"),
            },
        ),
    )

    def get_all_groups(self, obj):
        return list(obj.groups.all().values_list("name", flat=True))

    get_all_groups.short_description = "係・役職"

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "groups":
            kwargs["queryset"] = request.user.groups
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    list_display = ("year", "get_full_name", "google_login", "livelog_login", "is_staff", "get_all_groups")
    list_display_links = ("year", "get_full_name")
    list_filter = ("year", "is_staff")
    search_fields = (
        "last_name",
        "first_name",
    )
    ordering = (
        "year",
        "furigana",
    )
    filter_horizontal = ("groups",)
    add_form = RegisterForm

    def get_deleted_objects(self, objs, request):
        for query in objs:
            if query.is_superuser:
                messages.error(request, "開発者アカウントは削除できません")
                deleted_objects, model_count, perms_needed, protected = super().get_deleted_objects(objs, request)
                protected = ["開発者アカウント"]
                return (deleted_objects, model_count, perms_needed, protected)
        return super().get_deleted_objects(objs, request)

    def delete_queryset(self, request, queryset):
        for query in queryset:
            if query.is_superuser:
                messages.error(request, "開発者アカウントは削除できません")
            else:
                query.delete()


admin.site.register(User, SuperuserUserAdmin)
admin.site.register(TestMail)
custom_admin_site.register(User, BasicUserAdmin)
