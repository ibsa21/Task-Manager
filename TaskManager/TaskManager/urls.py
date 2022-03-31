
from unicodedata import name
from django import views
from django.contrib import admin
from django.urls import path, include
from .import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_page, name = "homepage" ),
    path('profile/', include('projects.urls')),
    path('my-team/', include('Team.urls')),
]
