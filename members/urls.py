from django.urls import path
from .views import (
    index,
    profile,
    test_mail,
    invitation_list,
    edit_invitation,
    delete_invitation,
)

urlpatterns = [
    path("", index, name="index"),
    path("profile/", profile, name="profile"),
    path("test_mail/", test_mail, name="test_mail"),
    path("invite/", invitation_list, name="invitation_list"),
    path("invite/<int:invitation_id>/", edit_invitation, name="edit_invitation"),
    path(
        "invite/<int:invitation_id>/delete/",
        delete_invitation,
        name="delete_invitation",
    ),
]

app_name = "members"
