from django.urls import path
from . import views

app_name = 'board'
urlpatterns = [
    # apis
    path('json/', views.get_messages_list),
    path('content/<int:id>/', views.get_one_message),
    path('contentothers/<int:id>/', views.get_message_attachments),
    path('bookmark/<int:pk>/', views.bookmarkAPI),
    path('send/togroups/', views.to_groups_data),
    path('send/froms/', views.froms_data),
    path('send/send/', views.sendAPI),

    # path('download/<int:message_pk>/<int:file_pk>/', views.FileDownloadView, name='attachment_DL'),
]
