from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='kansou_index'),
    path('upload/', views.KansouUpload, name='kansou_upload')
]
