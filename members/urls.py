from django.urls import path
from . import views
from config.views import SPA

app_name = 'members'
urlpatterns = [
    path('', SPA, name='index'),
    path('info-update/', SPA, name='update'),
    path('mail-settings/', SPA, name='mail_settings'),
    path('mail-test/', SPA, name='email_confirm'),
    path('oauth/', SPA, name='oauth'),
    path('sendbox/', SPA, name='sendbox'),
    path('register/', SPA, name='register_form'),
    
    path('api/user/', views.getUserInfo, name='api_get_user'),
    path('api/google_unlink/', views.googleOauthUnlink),
    path('api/info-update/', views.userUpdateAPI),
    path('api/mail-settings/', views.mailSettingsAPI),
    path('api/mail-test/', views.mailTestAPI),
    path('api/register/', views.registerAPI),
]
