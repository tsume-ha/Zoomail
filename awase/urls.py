from django.urls import path
from . import views

app_name = 'awase'
urlpatterns = [
	path('', views.index, name='awase_index'),
	path('calendar/<int:pk>/', views.CalendarView, name='awase_calendar'),
	path('calendar/<int:pk>/input/', views.input, name='input_top'),
	path('calendar/<int:pk>/input/<int:page>/', views.input, name='input'),
	path('create/', views.create, name='awase_create'),
]
