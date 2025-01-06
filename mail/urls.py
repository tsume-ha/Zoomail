from django.urls import path
from .views import inbox, mail_detail

urlpatterns = [
    path("", inbox, name="inbox"),
    path("/<int:message_id>/", mail_detail, name="mail_detail"),
]
