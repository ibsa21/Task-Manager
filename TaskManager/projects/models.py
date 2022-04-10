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

#Create Base class
class BaseModel(models.Model):
    project_name = models.CharField(max_length=20)
    project_description = models.TextField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    count = models.IntegerField(null=False, default=0)

    class Meta:
        abstract = True

#Personal Projects Model
class PersonalProjects(BaseModel):

    class Meta:
        ordering = ['created', 'updated']
    def __str__(self):
        return self.project_name

#create group project
class GroupProject(BaseModel, models.Model):
    members = models.ManyToManyField(User, blank = True,  related_name='members')
    deadline_date = models.DateTimeField()


    def get_member_count(self, pk):
        return GroupProject.objects.filter(id=pk).count()

    def __str__(self):
        return self.project_name


#Task Base Model
class Task(models.Model):
    task_name = models.CharField(max_length=50)
    description = models.TextField()
    deadline_date = models.DateTimeField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField()

    class Meta:
        abstract = True

#personal task models
class PersonalTask(Task, models.Model):
    project = models.ForeignKey(PersonalProjects, on_delete=models.CASCADE)
    user_name = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):

        if self.deadline_date < timezone.now():
            raise ValidationError (f'Deadline date cannot be before {{timezone.now()}}' )
        super(PersonalTask, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.task_name

#Group Task
class GroupTask(Task, models.Model):
    project = models.ForeignKey(GroupProject, on_delete=models.CASCADE)
    assignedTo = models.ManyToManyField(User, related_name="collaborators")

    def save(self, *args, **kwargs):
    
        if self.deadline_date < timezone.now():
            raise ValidationError (f'Deadline date cannot be before {{timezone.now()}}' )
        super(GroupTask, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.task_name

