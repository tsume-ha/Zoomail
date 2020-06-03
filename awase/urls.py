from django.urls import path
from . import views

app_name = 'awase'
urlpatterns = [
	path('', views.index, name='index'),
	path('calendar/<int:pk>/', views.CalendarView, name='calendar'),
	path('calendar/json/<int:pk>/', views.CalendarJsonResponse, name='calendar_json'),
	path('calendar/<int:pk>/input/', views.input, name='input'),
	path('calendar/json/<int:pk>/input/', views.inputJSON, name='input_json'),
	path('calendar/<int:pk>/urlkey/', views.CalendarURLKey, name='url_key'),
	path('create/', views.create, name='create'),
	path('invited/key=<str:key>/', views.invited, name='invited'),
	path('update/calendar/<int:pk>/', views.UpdateCalendarView, name='calendar_update'),
	path('update/hours/<int:pk>/', views.UpdateCollectHourView, name='hours_update_top'),
	path('update/hours/<int:pk>/page=<int:page>', views.UpdateCollectHourView, name='hours_update'),
	path('update/hours/json/<int:pk>/', views.CollectHourJsonResponse, name='hours_update_json'),
	path('update/user/<int:pk>/', views.ChangeUsers, name='change_users'),
	path('calendar/leave/<int:pk>/', views.LeaveCalendarView, name='leave_calendar'),
	path('calendar/delete/<int:pk>/', views.DeleteCalendarView, name='delete_calendar'),
	path('api/calendar/<int:pk>/', views.GetCalendarInfo, name='get_calendar_info'),

]
