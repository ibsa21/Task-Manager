from dataclasses import field, fields
from pyexpat import model
from django.forms import ModelForm
from .models import GroupProject, PersonalTask, Task, PersonalProjects

#personal Project Form
class PersonalProjectForm(ModelForm):

    class Meta:

        model = PersonalProjects
        fields = [
            'project_name',
            'project_description',
        ]

#Group Project Form
class GroupProjectForm(ModelForm):

    class Meta:

        model = GroupProject
        fields = [
            'project_name',
            'project_description',
            'deadline_date',
        ]

#personal Task Form
class PersonalTaskForm(ModelForm):
    class Meta:

        model =  PersonalTask
        fields = [
            'task_name', 
            'description',
            'deadline_date',
        ]

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = '__all__'