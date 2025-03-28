from django.urls import path
from django.views.generic import TemplateView

app_name = "howto"

urlpatterns = [
    path("", TemplateView.as_view(template_name="howto/index.html"), name="index"),
    path(
        "hajimeni/",
        TemplateView.as_view(template_name="howto/hajimeni.html"),
        name="hajimeni",
    ),
    path(
        "login/",
        TemplateView.as_view(template_name="howto/login.html"),
        name="login",
    ),
]
