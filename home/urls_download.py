from django.urls import path, include

from board.views import AttachmentDownloadView
from sound.views import SongDownloadView


urlpatterns = [
    path('mail/<int:message_id>/<int:attachment_id>/', AttachmentDownloadView),
    path('sound/<int:song_id>/', SongDownloadView),
]