from django.urls import path, include
from .views import homeAPI, tempUser, firstRegisterAPI

app_name = "api"
urlpatterns = [
    path("tempuser/", tempUser, name="tempuser"),
    path("first-register/", firstRegisterAPI, name="first_register_api"),
    path("home/index/", homeAPI),
    path("board/", include("board.urls")),
    path("mypage/", include("members.urls")),
    path("meeting_room/", include("meeting_room.urls")),
    path("photo/", include("pictures.urls")),
    path("sound/", include("sound.urls")),
    path("kansou/", include("kansou.urls")),
    path("movie/", include("movie.urls")),
    path("others/", include("otherdocs.urls")),
    path("mail/", include("mail.urls")),
]
