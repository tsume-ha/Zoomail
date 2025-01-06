from django.urls import path
from .views import inbox, mail_detail, send

urlpatterns = [
    path("", inbox, name="inbox"),
    path("<int:message_id>/", mail_detail, name="mail_detail"),
    path("send/", send, name="send"),
]

app_name = "mail"
