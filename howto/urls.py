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
        "login/", TemplateView.as_view(template_name="howto/login.html"), name="login"
    ),
    path(
        "mailtest/",
        TemplateView.as_view(template_name="howto/mailtest.html"),
        name="mailtest",
    ),
    path(
        "mailview/",
        TemplateView.as_view(template_name="howto/mailview.html"),
        name="mailview",
    ),
    path(
        "mailsend/",
        TemplateView.as_view(template_name="howto/mailsend.html"),
        name="mailsend",
    ),
    path(
        "userinfo/",
        TemplateView.as_view(template_name="howto/userinfo.html"),
        name="userinfo",
    ),
]
