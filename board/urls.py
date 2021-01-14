from django.urls import path
from . import views

app_name = 'board'
urlpatterns = [
    # apis
    path('api/json/', views.indexJsonResponse, name='messages_json'),
    path('api/content/<int:id>/', views.contentJson, name='content_json'),
    path('api/contentothers/<int:id>/', views.contentOtherData, name='content_other_json'),
    path('api/bookmark/<int:pk>/', views.bookmarkJson, name='bookmark_json'),
    path('api/send/togroups/', views.toGroups, name="send_to_groups"),
    path('api/send/froms/', views.froms, name="send_froms"),

    # new pages
    path('', views.index, name='read'),
    path('content/<int:message_pk>/attachment/<int:file_pk>/', views.FileDownloadView, name='attachment_DL'),

    # from mypage
    path('content/<int:id>', views.index, name='content'),

    # old pages
    # path('old', views.index, name='read'),
    # path('old/<int:page_num>/', views.index, name='page'),
    # path('old/content/<int:id>', views.content, name='content'),
    # path('old/content/<int:id>/edit/', views.edit, name='content_edit'),
    # path('old/ajax_bookmark/<int:pk>/', views.ajax_bookmark, name='ajax_bookmark'),


    path('download/<int:message_pk>/<int:file_pk>/', views.FileDownloadView, name='attachment_DL'),

    path('<path:p>/', views.index),
]
