from django.urls import path
from . import views

app_name = 'board'
urlpatterns = [
    # apis
    path('json/', views.indexJsonResponse, name='messages_json'),
    path('content/<int:id>/', views.contentJson, name='content_json'),
    path('contentothers/<int:id>/', views.contentOtherData, name='content_other_json'),
    path('bookmark/<int:pk>/', views.bookmarkJson, name='bookmark_json'),
    path('send/togroups/', views.toGroups, name="send_to_groups"),
    path('send/froms/', views.froms, name="send_froms"),
    path('send/send/', views.sendAPI, name="sendAPI"),

    path('download/<int:message_pk>/<int:file_pk>/', views.FileDownloadView, name='attachment_DL'),
]
