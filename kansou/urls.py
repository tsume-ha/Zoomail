from django.urls import path
from . import views

app_name = 'kansou'
urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.KansouUpload, name='upload')
]
