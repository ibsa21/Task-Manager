from django.urls import path, include
from . import views

urlpatterns = [
    path('my-team/', views.team_home,  name = 'my-team'),
]