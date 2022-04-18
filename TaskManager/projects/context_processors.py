# from collections import UserList
from .models import Task, PersonalProjects
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from json import dumps

#personal projects show page
def access_personal_projects(request):
    list_projects  = PersonalProjects.objects.filter(created_by = request.user.id)
    return {'personalProjects': list_projects, 'count':list_projects.count()}

def access_all_user(request):
    all_user = User.objects.all()
    user_dict = {}
    for user in all_user:
        user_dict[f'{user.id}'] = user.username
    user_list_json = dumps(user_dict)
    return {'all_user':user_list_json}