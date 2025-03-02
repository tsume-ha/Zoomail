from django.urls import path
from .views import index, profile, test_mail

urlpatterns = [
    path("", index, name="index"),
    path("profile/", profile, name="profile"),
    path("test_mail/", test_mail, name="test_mail"),
]

app_name = "members"
