from cgi import print_arguments
from django.shortcuts import render
from projects.models import GroupProject, PersonalTask, PersonalProjects, GroupTask
from projects.views import get_default_context
# Create your views here.


def team_home(request):
    group_project = GroupProject.objects.filter(created_by=request.user)
    context = {}

    if group_project:
        context = get_default_context(group_project[0].id, GroupTask, GroupProject)
        context['teams'] = group_project
    return render(request, 'dashboard/index.html', context)

def invite_team(request, pk):
    return render(request, 'dashboard/index.html', )
    