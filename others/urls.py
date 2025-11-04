from django.urls import path
from .views import file_list, file_edit, file_upload, file_download

app_name = "others"

urlpatterns = [
    path("", file_list, name="file_list"),
    path("upload/", file_upload, name="file_upload"),
    path("<int:pk>/edit/", file_edit, name="file_edit"),
    path("<int:pk>/download/", file_download, name="file_download"),
]
