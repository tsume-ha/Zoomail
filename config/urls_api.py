from django.urls import path,include

urlpatterns = [
    path('board/', include('board.urls')),
    path('mypage/', include('members.urls')),
    path('meeting_room/', include('meeting_room.urls')),
]