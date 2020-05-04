from django.urls import path
from . import views

app_name = 'howto'
urlpatterns = [
    path('', views.index, name='index'),
    path('introduction/', views.introduction, name='introduction'),
    path('user_setting/', views.user_setting, name='user_setting'),
    path('send_message/', views.send_message, name='send_message'),
]
