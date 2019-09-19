from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='player_index'),
	path('playlist/<int:live_id>', views.playlist, name='playlist'),
	path('songupload/', views.songupload, name='songupload'),
	# path('download/', views.download, name='download'),	
	path('download/playlist/<int:live_id>/<int:song_pk>', views.FileDownloadView, name='download'),
]
