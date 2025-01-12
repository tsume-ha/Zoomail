from django.urls import path
from .views import inbox, send, attachment

urlpatterns = [
    path("", inbox.inbox, name="inbox"),
    path("<int:id>/", inbox.detail, name="detail"),
    path(
        "<int:message_id>/attachments/<int:attachment_id>",
        attachment.download,
        name="attachment_download",
    ),
    path("send/", send.SendWizardView.as_view(), name="send"),
]

app_name = "mail"
