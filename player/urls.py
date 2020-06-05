from django.urls import path
from . import views

app_name = 'player'
urlpatterns = [
    path('', views.index, name='index'),
    path('playlist/<int:live_id>', views.playlist, name='playlist'),
    path('edit/<int:live_id>', views.edit, name='edit'),
    path('upload/', views.upload, name='upload'),
    path('download/playlist/<int:live_id>/<int:song_pk>',views.FileDownloadView, name='download'),
]
