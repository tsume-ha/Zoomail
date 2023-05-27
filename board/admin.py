from django.contrib import admin

from custom_admin.admin import custom_admin_site
from .models import Message, MessageYear, Attachment, Bookmark, ToGroup
from .forms import ToGroupAdminForm

class AttachmentAdmin(admin.StackedInline):
    model = Attachment
    extra = 0
    fields = ("attachment_file",)
    readonly_fields = ("attachment_file",)


class MessageYearAdmin(admin.StackedInline):
    model = MessageYear
    extra = 0
    fields = ("year",)
    readonly_fields = ("year",)


class BookmarkAdmin(admin.TabularInline):
    model = Bookmark
    extra = 0
    fields = ("user",)
    readonly_fields = ("user",)


class MessageSuperuserAdmin(admin.ModelAdmin):
    fields = ("title", "content", ("sender", "writer"), ("updated_at", "created_at"))
    readonly_fields = ("title", "content", "sender", "writer", "updated_at", "created_at")
    list_display = ("title", "years", "sender", "writer", "created_at", "sent_num", "error_num")
    list_display_links = ("title", "years")

    inlines = [MessageYearAdmin, AttachmentAdmin, BookmarkAdmin]

    def years(self, obj):
        return list(obj.years.all())

    def sent_num(self, obj):
        return obj.process.all().count()

    def error_num(self, obj):
        return obj.process.filter(Error_occurd=True).count()


class ToGroupAdmin(admin.ModelAdmin):
    model = ToGroup
    form = ToGroupAdminForm
    ordering = ["-year"]
    fields = ("year", "label", "leader")
    list_display = ("year", "label", "leader")

admin.site.register(Message, MessageSuperuserAdmin)
admin.site.register(ToGroup, ToGroupAdmin)
custom_admin_site.register(ToGroup, ToGroupAdmin)
