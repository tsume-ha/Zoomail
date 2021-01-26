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

    # # new pages
    # path('content/<int:message_pk>/attachment/<int:file_pk>/', views.FileDownloadView, name='attachment_DL'),

    # from mypage
    # path('content/<int:id>', views.index, name='content'),

    # # old pages
    # # path('old', views.index, name='read'),
    # # path('old/<int:page_num>/', views.index, name='page'),
    # # path('old/content/<int:id>', views.content, name='content'),
    # # path('old/content/<int:id>/edit/', views.edit, name='content_edit'),
    # # path('old/ajax_bookmark/<int:pk>/', views.ajax_bookmark, name='ajax_bookmark'),


    path('download/<int:message_pk>/<int:file_pk>/', views.FileDownloadView, name='attachment_DL'),
]
