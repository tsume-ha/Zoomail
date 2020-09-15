from django.urls import path
from . import views

app_name = 'board'
urlpatterns = [
    path('', views.index, name='read'),
    path('_/', views.index_, name='read_'),
    path('_/json/', views.indexJsonResponse, name='messages_json'),
    path('<int:page_num>/', views.index, name='page'),
    path('content/<int:id>', views.content, name='content'),
    path('content/<int:id>/edit/', views.edit, name='content_edit'),
    path('ajax_bookmark/<int:pk>/', views.ajax_bookmark, name='ajax_bookmark'),
    path('download/<int:message_pk>/<int:file_pk>/', views.FileDownloadView, name='attachment_DL')
]
