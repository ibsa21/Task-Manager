from cgi import print_arguments
from decimal import DefaultContext
from email import message
from email.headerregistry import Group
import imp
from multiprocessing import context
from typing import Counter
from django.shortcuts import redirect, render
from projects.forms import GroupProjectForm, GroupTaskForm
from projects.models import GroupProject, GroupMembers,  GroupTask
from projects.views import get_default_context
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.


def team_home(request):
    return render(request, 'dashboard/index.html', {'form':GroupTaskForm} )

def view_group_project(request, pk):
    context = get_default_context(pk, GroupTask, GroupProject)
    return render(request, 'dashboard/index.html', context)

def invite_team(request, pk):
    group_project = GroupProject.objects.get(id = pk)
    form = GroupProjectForm(instance = group_project)
    user = User.objects.get(username = request.POST['username'])
    list_members  = GroupMembers.objects.filter(project_id = pk).only('member_id')

    for member in list_members:

        if str(member)==str(user.username):
            messages.add_message(request, messages.INFO, f'{user} is already a member')
            return render(request, 'dashboard/index.html', get_default_context(pk, GroupTask, GroupProject))
            
    
    if request.method == "POST":

        obj = form.save(commit=False)
        obj.members.add(user)
        obj.save()

        form = GroupProjectForm()
        messages.add_message(request, messages.SUCCESS, f'Inviation is sent to {user}')

    return render(request, 'dashboard/index.html', get_default_context(pk, GroupTask, GroupProject))