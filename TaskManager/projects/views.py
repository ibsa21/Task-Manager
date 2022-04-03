from collections import UserDict
from multiprocessing import context
from operator import index
from pyexpat import model
from urllib import request
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Task, TaskUser
from Team.models import Team
from .forms import TaskForm

# Create your views here.
@login_required(login_url='login')
def home(request):
    user  = User.objects.get(username = request.user)
    user_team = Team.objects.filter(members = user.id)
    return render(request, 'dashboard/index.html', {'teams':user_team})
    
@login_required(login_url='login')
def project_view(request):
    task_name = Task.objects.all().only('task_name')

    list_tasks = {}
    for task in task_name:
        list_tasks[f'{task}'] = TaskUser.objects.filter(task_id=task.id)
    
    return render(request, 'projects/project_home.html', {'contrib':list_tasks})

@login_required(login_url='login')
def show_task_detail(request, pk):
    print(pk)
    task_name = Task.objects.get(task_name=pk)
    return render(request, 'projects/Task_info.html', {'task':task_name})

def create_task(request):
    form = TaskForm()

    if request.method == 'POST':
        form = TaskForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('home')
    
    context = {'form':form}
    return render(request, 'projects/task_form.html', context)

#mark started task into inprogress task
@login_required(login_url='login')
def start_task(request):

    print(request.method == "POST")
    task_list = Task.objects.all()

    if request.method == "POST":
        id_list = request.POST.getlist('boxes')
        print(id_list )

        return redirect('homepage')
    else:
        return render(request, 'Team/my_profile.html')

@login_required(login_url='login')
def update_task(request, pk):
    pass

@login_required(login_url='login')
def delete_task(request, pk):
    pass

#show team tasks
@login_required(login_url='login')
def team_projects(request, pk):
    team_name = Team.objects.get(id=pk)
    team_tasks = Team.objects.get(id = pk)

    return render(
                    request, 'projects/team_tasks.html', 
                    {
                        'teamTasks':team_tasks.team_task.all() ,
                        'team_name':team_name
                        }
                  )
@login_required(login_url='login')
def task_todo(request, pk):
    print(pk)
    return render(request
    , 'projects/hello.html')