from django.contrib import admin
from .models import Task, PersonalTask, PersonalProjects, GroupProject, GroupTask
# Register your models here.

admin.site.register(PersonalTask)
admin.site.register(PersonalProjects)
admin.site.register(GroupProject)
admin.site.register(GroupTask)