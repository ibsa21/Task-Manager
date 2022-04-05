# from collections import UserList
from .models import Task, TaskUser, PersonalProjects
from Team.models import Team
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

#personal projects show page
def access_personal_projects(request):
    list_projects  = PersonalProjects.objects.filter(created_by = request.user.id)
    return {'personalProjects': list_projects, 'count':list_projects.count()}

def access_completed_task(request):
    filter_one = Q(task_status = 'C')
    filter_two = Q(assigned_to = request.user.id)
    completed_task = Task.objects.filter(filter_one & filter_two)
    return {'completed':completed_task, 'no_completed':len(completed_task)}

def access_inprogress_task(request):
    filter_one = Q(task_status = 'I')
    filter_two = Q(assigned_to = request.user.id)
    inprogress = Task.objects.filter(filter_one & filter_two)
    return {'inprogress':inprogress, 'no_inprogress':len(inprogress)}
    
def access_todo_task(request):
    filter_one = Q(task_status = 'TD')
    filter_two = Q(assigned_to = request.user.id)
    todo_task = Task.objects.filter(filter_one & filter_two)
    return {'todoTasks':todo_task, 'no_todo':len(todo_task)}

def return_user(request):
    user_list = User.objects.all()
    return {'user_list':user_list}