from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='mypage_index'),
	path('mypage/<int:url_user_pk>', views.Mypage, name='mypage'),
	path('register/', views.UserRegistration, name='register_form'),
	path('register/csv/', views.UserRegistrationCSV, name='register_CSV'),
	path('register/csv/preview/', views.UserRegistrationPreview, name='register_preview'),
]
