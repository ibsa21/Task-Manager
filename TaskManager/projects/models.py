from email import message
from django.utils import timezone
from argparse import BooleanOptionalAction
from asyncio.windows_events import NULL
import datetime
from email.policy import default
from enum import unique
from pyexpat import model
from tkinter import CASCADE
from urllib import request
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib import messages
# Create your models here.

#Personal Projects Model
class PersonalProjects(models.Model):
    project_name = models.CharField(max_length=20)
    project_description = models.TextField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created', '-updated']
    def __str__(self):
        return self.project_name


#personal task models
class PersonalTask(models.Model):
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
    project = models.ForeignKey(PersonalProjects, on_delete=models.CASCADE)
    user_name = models.ForeignKey(User, on_delete=models.CASCADE)
    # start_date = models.DateTimeField()
    deadline_date = models.DateTimeField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    task_status = models.CharField(max_length=2, choices=status_choice, default=TODO)

    def save(self, *args, **kwargs):
    
        if self.deadline_date < timezone.now():
            raise ValidationError (f'Deadline date cannot be before {{timezone.now()}}' )
        super(PersonalTask, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.task_name

# group_task model
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
    start_date = models.DateTimeField()
    deadline_date = models.DateTimeField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    task_status = models.CharField(max_length=2, choices=status_choice, default=TODO)
    
    def __str__(self):
        return self.task_name
    

class TaskUser(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE )

    class Meta:
        unique_together = [['user_id', 'task_id']]

