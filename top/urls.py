from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import top_page_view

urlpatterns = [
    path("first_register/", top_page_view, name="first_register"),
    path("", login_required(top_page_view), name="top_page"),
]

app_name = "top"
