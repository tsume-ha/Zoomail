from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='pictures_index'),
    # path('upload/', views.KansouUpload, name='kansou_upload')
]
