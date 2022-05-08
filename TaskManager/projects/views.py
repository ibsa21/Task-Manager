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
from .models import GroupProject, GroupTask, PersonalTask, PersonalProjects
from .forms import GroupProjectForm, GroupTaskForm, TaskForm, PersonalProjectForm, PersonalTaskForm

# Create your views here.
@login_required(login_url='login')
def home(request):
    user  = User.objects.get(username = request.user)
    user_team = GroupProject.objects.filter(members = user.id)
    return render(request, 'dashboard/index.html', {'teams':user_team})
    
@login_required(login_url='login')
def project_view(request):
    task_name = PersonalTask.objects.all().only('task_name')

    list_tasks = {}
    for task in task_name:
        list_tasks[f'{task}'] = PersonalTask.objects.filter(id=task.id)
    
    return render(request, 'projects/project_home.html', {'contrib':list_tasks})

#generic function/ get_default_context
#generic function/ get defualt project
class DefaultProject:

    def __init__(self, task_model, project_model, pk, user_id) -> None:
        filter_project = Q(created_by = user_id)
        self.filter_one = Q(project = pk)
        self.filter_two = Q(is_completed = False)
        self.filter_three = Q(is_completed = True)

        self.pending = task_model.objects.filter(self.filter_one & self.filter_two)
        self.completed = task_model.objects.filter(self.filter_one & self.filter_three)
        self.project = project_model.objects.get(id=pk)
        self.context = {}
    
    #get all projects
    def get_all_projects(self):
        return self.project.objects.filter(self.filter_project)
    #get project
    def get_project(self):
        return self.project
    
    #get pending task
    def get_pending_task(self):
        return self.pending
    
    #get completed task
    def get_completed_task(self):
        return self.completed

    #get count of pending task
    def get_count_pending(self):
        return self.completed
    
    #get count of completed task
    def get_count_completed(self):
        return self.completed.count()
    
    # get count of pending task
    def get_count_pending(self):
        return self.pending.count()
    
    # get context
    def get_context(self, project_type:str):

        self.context['pending'] = self.get_pending_task
        self.context['completed'] = self.get_completed_task
        self.context['count_pending'] = self.get_count_pending
        self.context['count_completed'] = self.get_count_completed
        self.context[f'{project_type}_default'] = self.get_project
        self.context['projects'] = self.get_all_projects

        return self.context

def get_default_context(pk, model_object, default_ctx):

        filter_one = Q(project = pk)
        filter_two = Q(is_completed = False)
        filter_three = Q(is_completed = True)

        pending = model_object.objects.filter(filter_one & filter_two)
        completed = model_object.objects.filter(filter_one & filter_three)
        
        context = {
            
            'pending': pending, 
            'count_pending':pending.count(),

            'completed':completed,
            'count_completed':completed.count(),
            'default':default_ctx.objects.get(id=pk),
        }

        return context

#show personal projects homepage
@login_required(login_url='login')
def show_personal_projects(request, pk):
    project = PersonalProjects.objects.get(id=pk)

    if request.user == project.created_by:
        personal_project = DefaultProject(PersonalTask, PersonalProjects, pk, request.user.id)
        context  = personal_project.get_context('personal')
        if request.method =="POST":
            if 'project_name' in request.POST:
                create_personalProject(request, request.user)
            elif 'task_name' in request.POST:
                create_personalTask(request, pk)
        else:
            pass
    else:
        messages.error(request, 'Requested anauthorized page')
    print(context)
    return render(request, 'projects/project_page.html', context)

#show all personal projects
@login_required(login_url='login')
def default_personalProject(request):
    All_projects  = PersonalProjects.objects.filter(created_by = request.user.id)

    context = {}
    if All_projects:
        personal_project = DefaultProject(PersonalTask, PersonalProjects, All_projects[0].id,request.user.id)
        context = personal_project.get_context('personal')

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

#create project

def create_group_project(request):
    user_id  = request.user
    form = GroupProjectForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        
        #associating the current user with database table(PersonalProjects)
        obj = form.save(commit = False)
        obj.created_by = user_id
        obj.save()

        form = GroupProjectForm()
        messages.success(request, "Successfully created")
        return  redirect('projects')

    return render(request, 'dashboard/index.html')

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

@login_required(login_url='login')
def create_group_task(request, pk):
    requested_project = GroupProject.objects.get(id  = pk)

    if requested_project.created_by == request.user:
        form  = GroupTaskForm(request.POST or None, request.FILES or None)
        # form  = None
        if form.is_valid():
            obj = form.save(commit=False)
            obj.project = requested_project
            obj.is_completed = False
            obj.save()

            colloborators = list(map(int, request.POST.getlist('assignedTo')))
            obj = GroupTask.objects.get(id = obj.id)
            obj.assignedTo.set(id for id in colloborators)
            obj.save()
                            
            form = GroupTaskForm()
            requested_project.count = GroupTask.objects.filter(project = requested_project).count()
            requested_project.save()
            
        messages.add_message(request, messages.INFO, f"{obj} task is added")

    else:
        print("hello")
        messages.add_message(request, messages.INFO, "YOu are not authorized to create a task")
    return render(request, 'dashboard/index.html', get_default_context(pk, GroupTask, GroupProject))

#delete personal Project
def delete_personalProject(request, pk):
    project  = PersonalProjects.objects.get(id = pk)

    if request.method == 'POST':

        # project_tasks = PersonalTask.objects.filter(project=project)
        project.delete()
    
    return render(request, 'projects/project_page.html', {'obj':project})

#generic function/deleting task
def delete_task(request, task_model_name, project_model_name,  pk):
    task = task_model_name.objects.get(id = pk)
    project  = project_model_name.objects.get( id = task.project_id)

    if request.method == "POST":
        task.delete()

        #reducing number of counts
        project.count -=1
        project.save()
        return True
    return False

#delete personal Task
@login_required(login_url='login')
def delete_personalTask(request, pk):
    delete_task(request, PersonalTask, PersonalProjects, pk)
    return render(request, 'projects/project_page.html')

def delete_group_task(request, pk):
    delete_task(request, GroupTask, GroupProject, pk)
    return render(request, 'dashboard/index.html')

#search project functionality 
@login_required(login_url='login')

def search_projects(request):

    query = request.GET.get('query') if request.GET.get('query') is not None else ''
    try:
        context = {}
        project = PersonalProjects.objects.get(Q(project_name__icontains = query))
        if project.created_by == request.user:
            personal_project  = DefaultProject(PersonalTask, PersonalProjects, project.id, request.user.id)
            context = personal_project.get_context('personal')
        return render(request, 'projects/project_page.html', context)

    except Exception as e:
        return render(request, 'projects/project_page.html', {})

#generic function/ updating task
def update_task(request, model_name, form_name, pk):
    task = model_name.objects.get(id=pk)
    form = form_name(instance = task)

    if request.method == "POST":
        form = form_name(request.POST, instance=task)
        if form.is_valid():
            form.save()
            redirect(request.META['HTTP_REFERER'])
    return form

#edit tasks pt(personal_task)
def update_personalTask(request, pk):
    form = update_task(request, PersonalTask, PersonalTaskForm, pk)
    context = {'form':form}
    return render(request, 'projects/pt_form.html', context)

#update - group task
def update_group_task(request, pk):
    update_task(request, GroupTask, GroupTaskForm, pk)

    return render(request, 'dashboard/index.html')

#generic function/mark_completed
def mark_completed(request, task_model_name, project_model_name, pk):
    task = task_model_name.objects.get(id = pk)
    project = project_model_name.objects.get(id = task.project.id)

    if request.method == "POST":
        task.is_completed = True
        task.save()
    
    return project

#mark_completed personal task
@login_required(login_url='login')
def mark_completed_personaltask(request, pk):
    project = mark_completed(request, PersonalTask, PersonalProjects, pk)
    
    return render(request, 'projects/project_page.html', get_default_context(project.id, PersonalTask,  PersonalProjects))

#mark_completed group task
@login_required(login_url='login')
def mark_completed_grouptask(request, pk):
    mark_completed(request, GroupTask, GroupProject, pk)
    return redirect(request.META['HTTP_REFERER'])

    

@login_required(login_url='login')
def show_task_detail(request, pk):
    print(pk)
    task_name = PersonalTask.objects.get(task_name=pk)
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
    task_list = PersonalTask.objects.all()

    if request.method == "POST":
        id_list = request.POST.getlist('boxes')
        print(id_list )

        return redirect('homepage')
    else:
        return render(request, 'Team/my_profile.html')

#show team tasks
@login_required(login_url='login')
def team_projects(request, pk):
    team_name = GroupProject.objects.get(id=pk)
    team_tasks = GroupProject.objects.get(id = pk)

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