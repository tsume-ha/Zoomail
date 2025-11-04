from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import messages
from social_django.models import UserSocialAuth
from custom_admin.admin import custom_admin_site
from .models import User, TestMail


class SuperuserUserAdmin(BaseUserAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "year",
                    "fullname",
                    "nickname",
                    "furigana",
                    "email",
                    "livelog_email",
                    "receive_email",
                )
            },
        ),
        (("Permissions"), {"fields": (("is_staff", "is_superuser"), "groups")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "fullname", "year", "furigana"),
            },
        ),
    )

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
        "fullname",
        "google_oauth",
        "livelog_oauth",
        "is_staff",
        "is_superuser",
        "send_mail",
    )
    list_display_links = ("year", "fullname")
    list_filter = ("year", "is_staff", "is_superuser", "send_mail")
    search_fields = ("fullname", "email")
    ordering = (
        "year",
        "furigana",
    )

    def has_add_permission(self, request):
        return False

    # アプリ一覧（index）から “追加” 権限を消す
    def get_model_perms(self, request):
        perms = super().get_model_perms(request)
        perms["add"] = False
        return perms


class BasicUserAdmin(BaseUserAdmin):
    fieldsets = (
        (
            None,
            {"fields": ("year", "fullname", "nickname", "furigana")},
        ),
        (("Permissions"), {"fields": ("is_staff",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "fullname", "year", "furigana"),
            },
        ),
    )

    list_display = (
        "year",
        "fullname",
        "google_login",
        "livelog_login",
        "is_staff",
    )
    list_display_links = ("year", "fullname")
    list_filter = ("year", "is_staff")
    search_fields = (
        "fullname",
        "email",
    )
    ordering = (
        "year",
        "furigana",
    )

    def has_add_permission(self, request):
        return False

    # アプリ一覧（index）から “追加” 権限を消す
    def get_model_perms(self, request):
        perms = super().get_model_perms(request)
        perms["add"] = False
        return perms

    def get_deleted_objects(self, objs, request):
        for query in objs:
            if query.is_superuser:
                messages.error(request, "開発者アカウントは削除できません")
                deleted_objects, model_count, perms_needed, protected = (
                    super().get_deleted_objects(objs, request)
                )
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
