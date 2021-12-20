from django.urls import path, include

from board.views import AttachmentDownloadView

urlpatterns = [
    path('mail/<int:message_id>/<int:attachment_id>/', AttachmentDownloadView)
]