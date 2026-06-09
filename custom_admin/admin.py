from django.contrib import messages
from django.contrib import admin
from django.contrib.auth.models import Group
from django.shortcuts import render

from .forms import GroupAdminForm


class CustomAdminSite(admin.AdminSite):
    site_header = "Zoomail 管理者用ページ"

    class StaffPermissionAdminMixin:
        def _has_explicit_permission_override(self, method_name):
            for cls in type(self).mro()[2:]:
                if cls is admin.ModelAdmin:
                    return False
                if method_name in cls.__dict__:
                    return True
            return False

        def _has_custom_admin_permission(self, request):
            return request.user.is_active and request.user.is_staff

        def has_module_permission(self, request):
            if self._has_explicit_permission_override("has_module_permission"):
                return super().has_module_permission(request)
            return self._has_custom_admin_permission(request)

        def has_view_permission(self, request, obj=None):
            if self._has_explicit_permission_override("has_view_permission"):
                return super().has_view_permission(request, obj)
            return self._has_custom_admin_permission(request)

        def has_change_permission(self, request, obj=None):
            if self._has_explicit_permission_override("has_change_permission"):
                return super().has_change_permission(request, obj)
            return self._has_custom_admin_permission(request)

        def has_add_permission(self, request):
            if self._has_explicit_permission_override("has_add_permission"):
                return super().has_add_permission(request)
            return self._has_custom_admin_permission(request)

        def has_delete_permission(self, request, obj=None):
            if self._has_explicit_permission_override("has_delete_permission"):
                return super().has_delete_permission(request, obj)
            return self._has_custom_admin_permission(request)

    def register(self, model_or_iterable, admin_class=None, **options):
        admin_class = admin_class or admin.ModelAdmin
        if not issubclass(admin_class, self.StaffPermissionAdminMixin):
            admin_class = type(
                f"Custom{admin_class.__name__}",
                (self.StaffPermissionAdminMixin, admin_class),
                {"__module__": admin_class.__module__},
            )
        return super().register(model_or_iterable, admin_class, **options)

    def password_change(self, request, extra_context=None):
        messages.error(request, "Zoomailではパスワードを設定しません")
        return render(request, "registration/password_change_form.html")


custom_admin_site = CustomAdminSite(name="custom_admin")


# class GroupBasicAdmin(admin.ModelAdmin):
#     fieldsets = (
#         (
#             None,
#             {
#                 "fields": ("name", "users"),
#                 "description": "「利用可能 users」から係に登録したい人を選んで「選択された users 」に移動させてください。<br>"
#                 + "自分自身を係から外すと、このページに戻ることができなくなるので注意してください。",
#             },
#         ),
#     )
#     readonly_fields = ("name",)
#     form = GroupAdminForm

#     def get_queryset(self, request):
#         return request.user.groups.all()


# custom_admin_site.register(Group, GroupBasicAdmin)
