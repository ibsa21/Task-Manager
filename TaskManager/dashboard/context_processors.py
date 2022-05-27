import imp
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from json import dumps
from projects.models import GroupProject, GroupTask
from projects.views import get_default_context

#get default page for group template
def get_default_group_page(request):
    # group_project = GroupProject.objects.filter(created_by=request.user)
    # context = {}

    # if group_project:
    #     context = get_default_context(group_project[0].id, GroupTask, GroupProject)
    #     context['teams'] = group_project
    return {}