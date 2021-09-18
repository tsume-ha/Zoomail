from django.urls import path
from django.urls import include
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.views.generic.base import TemplateView
from custom_admin.admin import custom_admin_site
from . import views as home
import private_storage.urls

# Superuser 用の管理サイト設定
def has_permission(request):
    return request.user.is_superuser
admin.site.has_permission = has_permission


urlpatterns = [
    path('db/', admin.site.urls),
    path('admin/', custom_admin_site.urls),
    path('auth/', include('social_django.urls', namespace='social')),
    path('private-media/', include(private_storage.urls), name="private_media"),
    
    path('', home.index, name='index'),
    path('first_register/', home.firstRegister, name='first-register'),
    path('login/', home.login, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),


    # API
    path('api/', include('home.urls_api')),

    # SPA
    path('<path:p>', login_required(TemplateView.as_view(template_name='SPA.html'))),
]

