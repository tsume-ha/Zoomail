from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('playlist/<int:live_id>', views.playlist, name='playlist'),
	path('songupload/', views.songupload, name='songupload'),
]
