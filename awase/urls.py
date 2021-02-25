from django.urls import path
from . import views
from config.views import SPA

app_name = 'awase'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', SPA, name='create'),# SPA
    path('invited/key=<str:key>/', views.invited, name='invited'),
    
    path('<int:pk>/', SPA, name='calendar'),# SPA
    path('<int:pk>/json/', views.CalendarJsonResponse, name='calendar_json'),
    path('<int:pk>/input/', SPA, name='input'),# SPA
    path('<int:pk>/input/json/', views.inputJSON, name='input_json'),
    path('<int:pk>/urlkey/', views.CalendarURLKey, name='url_key'),
    path('<int:pk>/update/', views.UpdateCalendarView, name='calendar_update'),
    path('<int:pk>/hours/', SPA, name='hours_update_top'),# SPA
    path('<int:pk>/hours/json/', views.CollectHourJsonResponse, name='hours_update_json'),
    path('<int:pk>/user/', views.ChangeUsers, name='change_users'),
    path('<int:pk>/leave/', views.LeaveCalendarView, name='leave_calendar'),
    path('<int:pk>/delete/', views.DeleteCalendarView, name='delete_calendar'),
    path('<int:pk>/complete/', views.complete, name='complete'),

    path('api/create/', views.createJson, name='create_json'),
    path('<int:pk>/api/info/', views.GetCalendarInfo, name='get_calendar_info'),

]
