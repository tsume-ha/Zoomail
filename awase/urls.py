from django.urls import path
from . import views

app_name = 'awase'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('invited/key=<str:key>/', views.invited, name='invited'),
    
    path('<int:pk>/', views.CalendarView, name='calendar'),
    path('<int:pk>/json/', views.CalendarJsonResponse, name='calendar_json'),
    path('<int:pk>/input/', views.input, name='input'),
    path('<int:pk>/input/json/', views.inputJSON, name='input_json'),
    path('<int:pk>/urlkey/', views.CalendarURLKey, name='url_key'),
    path('<int:pk>/update/', views.UpdateCalendarView, name='calendar_update'),
    path('<int:pk>/hours/', views.UpdateCollectHourView, name='hours_update_top'),
    path('<int:pk>/hours/json/', views.CollectHourJsonResponse, name='hours_update_json'),
    path('<int:pk>/user/', views.ChangeUsers, name='change_users'),
    path('<int:pk>/leave/', views.LeaveCalendarView, name='leave_calendar'),
    path('<int:pk>/delete/', views.DeleteCalendarView, name='delete_calendar'),
    path('<int:pk>/api/info/', views.GetCalendarInfo, name='get_calendar_info'),

]
