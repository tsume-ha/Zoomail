from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='read'),
    path('content/<int:id>', views.content, name='content'),
    path('content/<int:id>/edit/', views.edit, name='message_edit'),
    path('ajax_bookmark/<int:pk>/', views.ajax_bookmark, name='message_ajax_bookmark'),
    path('download/<int:message_pk>/<int:file_pk>/', views.FileDownloadView, name='attachment_DL')
]
