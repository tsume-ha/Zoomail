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
    # path('register/', views.UserRegistration, name='register_form'),
    # path('register/csv/', views.UserRegistrationCSV, name='register_CSV'),
    # path('register/csv/preview/', views.UserRegistrationPreview, name='register_preview'),
    path('first_register/', views.NewFromLiveLog, name='new_from_livelog'),
    
    path('api/user/', views.getUserInfo, name='api_get_user'),
    path('api/google_unlink/', views.googleOauthUnlink),
    path('api/info-update/', views.userUpdateAPI),
    path('api/mail-settings/', views.mailSettingsAPI),
    path('api/mail-test/', views.mailTestAPI),
    
]
