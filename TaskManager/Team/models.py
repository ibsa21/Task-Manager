from email.policy import default
from multiprocessing.reduction import AbstractReducer
from pickle import TRUE
from projects.models import Task, TaskUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User, AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models

class Team(models.Model):

    team_name = models.CharField(max_length=20)
    team_desciption = models.TextField(max_length=100)
    members = models.ManyToManyField(User, related_name="users")
    team_task = models.ManyToManyField(Task, related_name="team_tasks")
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.team_name
    

#now create a team model