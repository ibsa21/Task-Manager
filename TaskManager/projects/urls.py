from django.conf import settings
from django.conf.urls.static import static
from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = "home"),
    path('task/<str:pk>/', views.show_task_detail, name = "task_detail"),
    path('update-task/<str:pk>/', views.update_task, name = "update_task"),
    path('delete-task/<str:pk>/', views.update_task, name = "delete_task"),
    path('projects/', views.project_view, name = "projects" ),
    path('create-task/', views.create_task, name = 'create-task'),
    path('projects/start-task/', views.start_task, name = 'start-task'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)