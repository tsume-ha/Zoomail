from django.urls import path
from . import views

app_name = 'meeting-room'
urlpatterns = [
    path('', views.index, name='index'),

    path('delete/', views.delete, name='delete'),
    path('register/', views.register, name='register'),
    path('sync/', views.sync, name='sync'),

    path('get31day/', views.get31day),
    path('today/', views.today),
    path('get_all/', views.get_all),

]
