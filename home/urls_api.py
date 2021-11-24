from django.urls import path,include
from .views import homeAPI

urlpatterns = [
    path('home/index/', homeAPI),
    path('board/', include('board.urls')),
    path('mypage/', include('members.urls')),
    path('meeting_room/', include('meeting_room.urls')),
    path('photo/', include('pictures.urls')),
    path('sound/', include('sound.urls')),
    path('kansou/', include('kansou.urls')),
]