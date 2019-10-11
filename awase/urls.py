from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='awase_index'),
	path('calendar/<int:pk>/', views.calendar, name='awase_calendar'),
	path('calendar/<int:pk>/input/', views.input),
	path('create/', views.create, name='awase_create'),
]
