from django.urls import path
from . import views

app_name = "meeting-room"
urlpatterns = [
    path("meeting_room.ics", views.EventFeed()),
    # path("", views.index),
    # path("register/", views.register, name="register"),
    # path("sync/", views.sync, name="sync"),
    # path("", views.index),
    # path("get31day/", views.get31day),
    # path("today/", views.today),
    # path("get_all/", views.get_all),
]
