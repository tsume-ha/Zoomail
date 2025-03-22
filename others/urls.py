from django.urls import path
from .views import file_list, file_detail, file_upload

app_name = "others"

urlpatterns = [
    path("", file_list, name="file_list"),
    path("upload/", file_upload, name="file_upload"),
    path("<int:pk>/", file_detail, name="file_detail"),
]
