from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = "home"),
    path('projects/', views.project_view, name = "projects" ),
    path('create-task/', views.create_task, name = 'create-task')
]