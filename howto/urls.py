from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='howto_index'),
    path('user_setting/', views.user_setting,),
    path('send_message/', views.send_message,),
]
