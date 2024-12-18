from django.contrib import messages
from django.contrib import admin
from django.contrib.auth.models import Group
from django.shortcuts import render

from .forms import GroupAdminForm


class CustomAdminSite(admin.AdminSite):
    site_header = "Zoomail 管理者用ページ"

    def password_change(self, request, extra_context=None):
        messages.error(request, "Zoomailではパスワードを設定しません")
        return render(request, "registration/password_change_form.html")


custom_admin_site = CustomAdminSite(name="custom_admin")


class GroupBasicAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": ("name", "users"),
                "description": "「利用可能 users」から係に登録したい人を選んで「選択された users 」に移動させてください。<br>"
                + "自分自身を係から外すと、このページに戻ることができなくなるので注意してください。",
            },
        ),
    )
    readonly_fields = ("name",)
    form = GroupAdminForm

    def get_queryset(self, request):
        return request.user.groups


custom_admin_site.register(Group, GroupBasicAdmin)
