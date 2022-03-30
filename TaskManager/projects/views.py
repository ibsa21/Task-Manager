from operator import index
from django.shortcuts import render, redirect

# Create your views here.

def home(request):
    return render(request, 'index.html')

def project_view(request):
    return render(request, 'projects/project_home.html')
