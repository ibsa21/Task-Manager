from django.shortcuts import render, redirect

def home_page(request):
    return render(request, 'home_page.html')
    
def home(request):
    return render(request, 'index.html')