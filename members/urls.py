from django.urls import path
from . import views

app_name = 'members'
urlpatterns = [
    path('', views.index, name='index'),
    path('update/', views.UserUpdate, name='update'),
    path('register/', views.UserRegistration, name='register_form'),
    path('register/csv/', views.UserRegistrationCSV, name='register_CSV'),
    path('register/csv/preview/', views.UserRegistrationPreview, name='register_preview'),
]
