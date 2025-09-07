from django.urls import path
from .views import top_page_view

urlpatterns = [
    path("first_register/", top_page_view, name="first_register"),
    path("", top_page_view, name="top_page"),
]

app_name = "top"
