from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('content/<int:id>', views.content, name='content'),
    path('content/<int:id>/edit/', views.edit, name='message_edit'),

]
