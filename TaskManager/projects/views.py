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

#get default project for showing
def get_default_context(pk):
        filter_one = Q(project = pk)
        filter_two = Q(is_completed = False)
        filter_three = Q(is_completed = True)

        pending = PersonalTask.objects.filter(filter_one & filter_two)
        completed = PersonalTask.objects.filter(filter_one & filter_three)
        # ToDo = PersonalTask.objects.filter(filter_one & filter_three)
        
        context = {
            'pending': pending, 
            'count_pending':pending.count(),

            'completed':completed,
            'count_completed':completed.count(),

            'default':PersonalProjects.objects.get(id=pk),
        }

        return context

#show personal projects homepage
@login_required(login_url='login')
def show_personal_projects(request, pk):
    project = PersonalProjects.objects.get(id=pk)
    context = {}
    if request.user == project.created_by:
        context = get_default_context(pk)
        if request.method =="POST":
            if 'project_name' in request.POST:
                create_personalProject(request, request.user)
            elif 'task_name' in request.POST:
                create_personalTask(request, pk)
        else:
            pass
    else:
        messages.error(request, 'Requested anauthorized page')
    return render(request, 'projects/project_page.html', context)

#show all personal projects
@login_required(login_url='login')
def default_personalProject(request):
    All_projects  = PersonalProjects.objects.filter(created_by = request.user.id)
    
    context = {}
    if All_projects:
        context = get_default_context(All_projects[0].id)
        context['projects'] = All_projects

    return render(request, 'projects/project_page.html', context)


#create personal projects view
@login_required(login_url='login')
def create_personalProject(request):
    
    user_id  = request.user
    form = PersonalProjectForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        
        #associating the current user with database table(PersonalProjects)
        obj = form.save(commit = False)
        obj.created_by = user_id
        obj.save()

        form = PersonalProjectForm()
        messages.success(request, "Successfully created")
        return  redirect('projects')

    return render(request, 'projects/pp_form.html')

#create personal task
@login_required(login_url='login')
def create_personalTask(request, pk):
    form = PersonalTaskForm(request.POST or None, request.FILES or None)
    project = PersonalProjects.objects.get(id=pk)

    if form.is_valid():
        
        #associating the current user with database table(PersonalProjects)
        obj = form.save(commit = False)
        obj.user_name = request.user
        obj.is_completed = False
        obj.project = project
        obj.save()

        form = PersonalTaskForm()

        #update count of projects((this is how it's done)
        project.count = PersonalTask.objects.filter(project=project).count()
        project.save()
        
        messages.success(request, "Successfully created")
        return  redirect('projects')

    return render(request, 'projects/pt_form.html')

#edit tasks pt(personal_task)
def update_personalTask(request, pk):
    task = PersonalTask.objects.get(id = pk)

    form  = PersonalTaskForm(instance=task)
    if request.method == "POST":
        form = PersonalTaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form':form}
    return render(request, 'projects/pt_form.html', context)

#delete personal Project
def delete_personalProject(request, pk):
    project  = PersonalProjects.objects.get(id = pk)

    if request.method == 'POST':

        # project_tasks = PersonalTask.objects.filter(project=project)
        project.delete()
    
    return render(request, 'projects/project_page.html', {'obj':project})
    
#delete personal Task
@login_required(login_url='login')
def delete_personalTask(request, pk):
    task = PersonalTask.objects.get(id=pk)

    if request.method == "POST":
        task.delete()
    return render(request, 'projects/project_page.html')

# mark tasks completed
@login_required(login_url='login')
def mark_completed(request, pk):
    task = PersonalTask.objects.get(id = pk)

    if request.method == "POST":
        task.is_completed = True
        task.save()

    return render(request, 'projects/project_page.html')

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