from email import message
import email
from multiprocessing import context
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from projects.models import PersonalTask
from django.contrib.auth.decorators import login_required
from django.db.models import Q


def registration(request):
    
    if request.user.is_authenticated:
        return redirect('projects')
    else:
        form = CreateUserForm()

        if request.method == "POST":
            form = CreateUserForm(request.POST)

            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)
                return redirect('login')

        context = {'form':form}
        return render(request, 'Team/registration_form.html', context)


def login_page(request):
    if request.user.is_authenticated:
        return redirect('projects')
    else:
        if request.method=="POST":
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password = password)

            if user is not None:
                context = {'profile':user}
                print(context)
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'username or password is incorrect')

        return render(request, 'Team/login_form.html')


@login_required(login_url='homepage')
def search_user(request):
    query = request.GET.get('user') if request.GET.get('user') is not None else ''
    filter_one = Q(username__icontains = query)
    filter_two = Q(email = query)

    try:
        user = User.objects.get(filter_one | filter_two)
        return user
    except Exception as e:
        return render(request, 'dashboard/index.html', {})

@login_required(login_url='homepage')
def Team(request):
    return render(request, 'dashboard/index.html')

def logout_user(request):
    logout(request)
    return redirect('homepage')

#show - user profile
@login_required(login_url='homepage')
def show_profile(request):
    user_todo = []
    user_task_completed = []
    user_task_inprogress = []
    query = PersonalTask.objects.all()
    for queries in query:
        if queries.assigned_to == request.user:
            user_todo.append(queries)
    
    return render(request, 'Team/my_profile.html')