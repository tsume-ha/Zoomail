from django.urls import path
from django.urls import include
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from . import views as home
import private_storage.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('social_django.urls', namespace='social')),
    path('private-media/', include(private_storage.urls), name="private_media"),
    
    path('', home.index, name='index'),
    path('first_register/', home.firstRegister, name='first-register'),
    path('login/', home.login, name='login'),
    path('logout/', home.logoutview, name='logout'),


    # API
    path('api/', include('home.urls_api')),

    # SPA
    path('<path:p>', login_required(TemplateView.as_view(template_name='SPA.html'))),
]