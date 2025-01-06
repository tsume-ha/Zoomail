from django.contrib import admin

from custom_admin.admin import custom_admin_site
from .models import Message, Attachment, ToGroup

# from .forms import ToGroupAdminForm

# from utils.mail3 import MailisReSender
from django.contrib import messages


class AttachmentAdmin(admin.StackedInline):
    model = Attachment
    extra = 0
    fields = ("file",)
    readonly_fields = ("file",)


class MessageSuperuserAdmin(admin.ModelAdmin):
    fields = ("title", "content", ("sender", "writer"), ("updated_at", "created_at"))
    readonly_fields = (
        "title",
        "content",
        "sender",
        "writer",
        "updated_at",
        "created_at",
    )
    list_display = (
        "title",
        "years",
        "sender",
        "writer",
        "created_at",
        "sent_num",
        "error_num",
        "pending_num",
    )
    list_display_links = ("title", "years")

    inlines = [AttachmentAdmin]

    def years(self, obj):
        return list(obj.years.all())

    @admin.display(description="送信中")
    def pending_num(self, obj):
        return obj.logs.filter(status="pending").count()

    @admin.display(description="送信完了")
    def sent_num(self, obj):
        return obj.logs.filter(status="success").count()

    @admin.display(description="エラー")
    def error_num(self, obj):
        return obj.logs.filter(status="failed").count()

    @admin.action(description="選択したメーリスを再送信する")
    def resend_mail(self, request, queryset):
        pass
        # for message in queryset:
        #     sender = MailisReSender(message)
        #     count = sender.send()
        #     messages.add_message(
        #         request, messages.SUCCESS, f"メーリス「{message.title}」を{count}人に再送信しました。"
        #     )
        #     messages.add_message(request, messages.INFO, f"最新の状態を取得するには、ページを更新してください。")

    actions = [resend_mail]


# class ToGroupAdmin(admin.ModelAdmin):
#     model = ToGroup
#     form = ToGroupAdminForm
#     ordering = ["-year"]
#     fields = ("year", "label", "leader")
#     list_display = ("year", "label", "leader")


admin.site.register(Message, MessageSuperuserAdmin)
# admin.site.register(ToGroup, ToGroupAdmin)
# custom_admin_site.register(ToGroup, ToGroupAdmin)
