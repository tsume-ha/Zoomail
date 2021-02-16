from django.urls import path,include

urlpatterns = [
    path('board/', include('board.urls')),
    path('mypage/', include('members.urls')),
]