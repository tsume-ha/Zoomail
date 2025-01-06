from django.urls import path
from .views import inbox, detail, send

urlpatterns = [
    path("", inbox, name="inbox"),
    path("<int:id>/", detail, name="detail"),
    path("send/", send, name="send"),
]

app_name = "mail"
