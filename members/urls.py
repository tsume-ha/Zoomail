from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('mypage/<int:url_user_pk>', views.Mypage, name='mypage'),
	# path('mypage/<int:url_user_pk>/update/', views.UserUpdate,),
]
