from django.urls import path
from . import views
from django.views.generic.base import TemplateView

app_name = 'home'
urlpatterns = [
    path('', views.index, name='index'),
    path('_/', TemplateView.as_view(template_name='index.html')),
    path('first_register/', views.firstRegister, name='first-register'),
]
