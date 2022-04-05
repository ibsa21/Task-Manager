from dataclasses import field, fields
from pyexpat import model
from django.forms import ModelForm
from .models import PersonalTask, Task, PersonalProjects

#personal Project Form
class PersonalProjectForm(ModelForm):
    class Meta:

        model = PersonalProjects
        fields = [
            'project_name',
            'project_description',
        ]

#personal Task Form
class PersonalTaskForm(ModelForm):
    class Meta:

        model =  PersonalTask
        fields = [
            'task_name', 
            'description',
            'start_date',
            'deadline_date',
            'task_status'
        ]


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = '__all__'