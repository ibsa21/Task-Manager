from argparse import BooleanOptionalAction
from pyexpat import model
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Task(models.Model):
    task_name = models.CharField(max_length=50)
    description = models.TextField()
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField()
    deadline_date = models.DateTimeField()

    def __str__(self):
        return self.task_name
class CompletedTask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

class InprogressTask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
