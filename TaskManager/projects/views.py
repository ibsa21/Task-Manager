from multiprocessing import context
from operator import index
from pyexpat import model
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Task, CompletedTask, InprogressTask
from .forms import TaskForm

# Create your views here.

@login_required(login_url='login')
def home(request):
    return render(request, 'index.html')

@login_required(login_url='login')
def project_view(request):
    task = Task.objects.all()
    
    completed_task = CompletedTask.objects.all()
    inprogress = InprogressTask.objects.all()
    context = {'todoTasks':task, 'no_todo':len(task), 'completed':completed_task, 'no_completed':len(completed_task),  'inprogress':inprogress, 'no_inprogress':len(inprogress) }
    return render(request, 'projects/project_home.html', context)

@login_required(login_url='login')
def create_task(request):
    form = TaskForm()

    if request.method == 'POST':
        form = TaskForm(request.POST)

    if form.is_valid():
        form.save()
        return redirect('home')
    
    context = {'form':form}
    return render(request, 'projects/task_form.html', context)