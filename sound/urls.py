from django.urls import path
from . import views

app_name = 'sound'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:id>/', views.content, name='content'),
    # path('<int:live_id>/', SPA, name='playlist'),
    # path('<int:live_id>/json/', views.playlistJson, name='playlist_json'),
    # path('<int:live_id>/edit/', views.edit, name='edit'),
    # path('upload/', views.upload, name='upload'),
    # path('download/<int:song_pk>/', views.FileDownloadView, name='download'),
]
