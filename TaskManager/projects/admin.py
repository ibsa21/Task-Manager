from django.contrib import admin
from .models import Task, TaskUser, PersonalTask, PersonalProjects
# Register your models here.

admin.site.register(Task)
admin.site.register(TaskUser)
admin.site.register(PersonalTask)
admin.site.register(PersonalProjects)