# from collections import UserList
from .models import Task, PersonalProjects
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

#personal projects show page
def access_personal_projects(request):
    list_projects  = PersonalProjects.objects.filter(created_by = request.user.id)
    return {'personalProjects': list_projects, 'count':list_projects.count()}