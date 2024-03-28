from django.urls import path
from .views import MailStatusView

app_name = "board"
urlpatterns = [
    path("status/", MailStatusView.as_view(), name="mail_status"),
]
