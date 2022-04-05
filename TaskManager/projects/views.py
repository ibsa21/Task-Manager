from collections import UserDict
from multiprocessing import context
from operator import index
from pyexpat import model
from urllib import request
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Task, TaskUser, PersonalTask, PersonalProjects
from Team.models import Team
from .forms import TaskForm, PersonalProjectForm, PersonalTaskForm

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

#show personal projects homepage
@login_required(login_url='login')
def show_personal_projects(request, pk):
    requested_project_creater = PersonalProjects.objects.get(id=pk)
    context = {}
    if request.user == requested_project_creater.created_by:
        filter_one = Q(project = pk)
        filter_two = Q(task_status = 'C')
        filter_three = Q(task_status = 'TD')
        filter_four = Q(task_status = 'P')

        completed = PersonalTask.objects.filter(filter_one & filter_two)
        pending = PersonalTask.objects.filter(filter_one & filter_four)
        ToDo = PersonalTask.objects.filter(filter_one & filter_three)

        context = {
            'to_dos': ToDo, 
            'count_todos':ToDo.count(), 

            'pending': pending, 
            'count_pending':pending.count(),

            'completed':completed,
            'count_completed':completed.count(),

            'project_name':PersonalProjects.objects.get(id=pk),
        }
    else:
        messages.error(request, 'Requested anauthorized page')
    return render(request, 'projects/project_page.html', context)

#create personal projects view
@login_required(login_url='login')
def create_personalProject(request):
    form = PersonalProjectForm(request.POST or None, request.FILES or None)
    if request.method =='POST':
          
        if form.is_valid():
            
            #associating the current user with database table(PersonalProjects)
            obj = form.save(commit = False)
            obj.created_by = request.user
            obj.save()

            form = PersonalProjectForm()
            messages.success(request, "Successfully created")
            return  redirect('projects')

    context = {'form':form}
    return render(request, 'projects/pp_form.html', context)

#create personal task
@login_required(login_url='login')
def create_personalTask(request, pk):
    form = PersonalTaskForm(request.POST or None, request.FILES or None)
    project = PersonalProjects.objects.get(id=pk)
    task_list = PersonalTask.objects.filter(project=pk)
    if request.method =='POST':    
        if form.is_valid():
            
            #associating the current user with database table(PersonalProjects)
            obj = form.save(commit = False)
            obj.user_name = request.user
            obj.project = project
            obj.save()

            form = PersonalTaskForm()
            #create another project 
            messages.success(request, "Successfully created")
            return  redirect('projects')

    context = {'form':form , 'project_list':task_list}
    return render(request, 'projects/pt_form.html', context)
    

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