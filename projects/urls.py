from django.conf import settings
from django.conf.urls.static import static
from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = "home"),

    #all projects (personal + group)
    path('projects/', views.project_view, name = "projects" ),
    path('projects/ <str:pk>/', views.team_projects, name = "team_projects" ),
    path('projects/start-task/', views.start_task, name = 'start-task'),

    #personal projects link
    path('show-projects/', views.default_personalProject, name = 'show-pp' ),
    path('show-projects/<str:pk>', views.show_personal_projects, name = 'view-pp' ),
    path('personal-project/', views.create_personalProject, name = "create-pp"),
    path('group-project/', views.create_group_project, name = "add-group-project"),
    path('delete-pp/<str:pk>', views.delete_personalProject, name = "delete-pp"),
    path('delete-pt/<str:pk>', views.delete_personalTask, name = "delete-pt"),
    path('delete-grouptask/<str:pk>', views.delete_group_task, name = "delete-grouptask"),
    path('update-grouptask/<str:pk>', views.update_group_task, name = 'update-grouptask'),
    path('personal-task/<str:pk>', views.create_personalTask, name = "create-pt"),
    path('group-task/<str:pk>', views.create_group_task, name = "create-gt"),
    path('update-pt/<str:pk>', views.update_personalTask, name = "update-personalTask"),
    path('mark-task/<str:pk>/', views.mark_completed_personaltask, name = "mark-completed"),
    path('mark-grouptask/<str:pk>/', views.mark_completed_grouptask, name = "mark-completed-gt"),
    path('search-projects/', views.search_projects, name = 'search-project'),

    #task-links
    path('task/<str:pk>/', views.show_task_detail, name = "task_detail"),
    path('update-task/<str:pk>/', views.update_task, name = "update_task"),
    path('delete-task/<str:pk>/', views.update_task, name = "delete_task"),
    path('create-task/', views.create_task, name = 'create-task'),

    #another links
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)