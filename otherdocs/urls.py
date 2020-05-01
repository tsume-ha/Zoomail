from django.urls import path
from . import views

app_name = 'otherdocs'
urlpatterns = [
    path('', views.index, name='index'),
    path('download/<int:pk>/', views.FileDownloadView, name='download'),
    path('upload/', views.UploadView, name='upload'),
    path('edit/', views.EditIndexView, name='edit_index'),
    path('edit/<int:pk>/', views.EditView, name='edit'),
]
