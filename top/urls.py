from django.urls import path
from .views import top_page_view

urlpatterns = [
    path("", top_page_view, name="top_page"),
    path("", top_page_view, name="first_register"),
]
