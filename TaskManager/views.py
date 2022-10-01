from operator import imod
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

def home_page(request):
    return render(request, 'home_page.html')
    
def home(request):
    return render(request, 'index.html')