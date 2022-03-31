from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.Team,  name="My-team"),
    path('registration/', views.registration, name = "registration"),
    path('login/', views.login_page, name = "login"),
    path('logout/', views.logout_user, name = "logout"),
]