from django.urls import path
from . import views

app_name = "meeting-room"
urlpatterns = [
    path("get31day/", views.get31day),
    path("today/", views.today),
    path("get_by_month/", views.get_by_month),
    path("register/", views.register),
]
