from django.urls import path, include
from . import views

urlpatterns = [
    path('my-team/', views.team_home,  name = 'my-team'),
    path('invite/<str:pk>/', views.invite_team,  name = 'invite'),
    path('team-project/<str:pk>/', views.view_group_project, name = "view_group_project"),
]