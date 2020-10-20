"""u_message URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
import board.views as board
import home.views as home
import private_storage.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('login/', home.login, name='login'),
    path('logout/', home.logoutview, name='logout'),
    path('auth/', include('social_django.urls', namespace='social')),
    path('private-media/', include(private_storage.urls), name="private_media"),
    path('mypage/', include('members.urls')),
    path('read/', include('board.urls')),
    path('send/', board.send_, name="send"),
    # sendのAPIは全て/read/api/へ
    path('send_old/', board.send, name="send_old"),
    path('sound/', include('sound.urls')),
    path('kansou/', include('kansou.urls')),
    path('pictures/', include('pictures.urls')),
    path('movie/', include('movie.urls')),
    path('others/', include('otherdocs.urls')),
    path('special/<str:url>/', home.special),
    path('awase/', include('awase.urls')),
    path('howto/', include('howto.urls')),
]