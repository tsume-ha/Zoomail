from django.urls import path, include

from board.views import AttachmentDownloadView
from sound.views import SongDownloadView
from kansou.views import kansouDownloadView


urlpatterns = [
    path('mail/<int:message_id>/<int:attachment_id>/', AttachmentDownloadView),
    path('sound/<int:song_id>/', SongDownloadView),
    path('kansou/<int:kansou_id>/', kansouDownloadView),
]