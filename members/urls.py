from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='mypage_index'),
    path('update/', views.UserUpdate, name='user_update'),
    path('register/', views.UserRegistration, name='register_form'),
    path('register/csv/', views.UserRegistrationCSV, name='register_CSV'),
    path('register/csv/preview/', views.UserRegistrationPreview, name='register_preview'),
]
