from django.urls import path
from . import views
from config.views import SPA

app_name = 'members'
urlpatterns = [
    path('user/', views.getUserInfo, name='api_get_user'),
    path('google_unlink/', views.googleOauthUnlink),
    path('info-update/', views.userUpdateAPI),
    path('mail-settings/', views.mailSettingsAPI),
    path('mail-test/', views.mailTestAPI),
    path('register/', views.registerAPI),
]
