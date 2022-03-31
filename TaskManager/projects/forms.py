from dataclasses import fields
from pyexpat import model
from django.forms import ModelForm
from .models import Task

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = '__all__'