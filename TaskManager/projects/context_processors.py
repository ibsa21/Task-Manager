from .models import Task, TaskUser
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def access_completed_task(request):
    completed_task = Task.objects.filter(task_status = 'C')
    return {'completed':completed_task, 'no_completed':len(completed_task)}

@login_required(login_url='login')
def access_inprogress_task(request):
    inprogress = Task.objects.filter(task_status = 'P')
    return {'inprogress':inprogress, 'no_inprogress':len(inprogress)}
    
@login_required(login_url='login')
def access_todo_task(request):
    todo_task = Task.objects.filter(task_status = 'TD')
    return {'todoTasks':todo_task, 'no_todo':len(todo_task)}
