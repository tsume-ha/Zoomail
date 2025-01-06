from django.urls import path
from .views import inbox, send

urlpatterns = [
    path("", inbox.inbox, name="inbox"),
    path("<int:id>/", inbox.detail, name="detail"),
    path("send/", send.SendWizardView.as_view(), name="send"),
]

app_name = "mail"
