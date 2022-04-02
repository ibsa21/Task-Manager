from argparse import BooleanOptionalAction
from enum import unique
from pyexpat import model
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Task(models.Model):
    
    TODO = 'TD'
    COMPLETED = 'C'
    INPROGRESS = 'P'

    status_choice = [
        (TODO, 'Todo Task'),
        (COMPLETED, 'Completed Task'),
        (INPROGRESS, 'Inprogress Task'),
    ]

    task_name = models.CharField(max_length=50)
    description = models.TextField()
    assigned_to = models.ManyToManyField(User, through="TaskUser")
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField()
    deadline_date = models.DateTimeField()
    task_status = models.CharField(max_length=2, choices=status_choice, default=TODO)
    def __str__(self):
        return self.task_name
    

class TaskUser(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE )

    class Meta:
        unique_together = [['user_id', 'task_id']]