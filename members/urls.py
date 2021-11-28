from django.urls import path
from . import views

app_name = 'members'
urlpatterns = [
    path('user/', views.userInfo, name='api_get_user'),
    path('google_unlink/', views.googleOauthUnlink),
    path('profile/', views.profile),
    path('mail-settings/', views.mailSettingsAPI),
    path('mail-test/', views.mailTestAPI),
    path('register/', views.registerAPI),
]
