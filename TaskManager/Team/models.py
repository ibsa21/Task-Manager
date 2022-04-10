from email.policy import default
from multiprocessing.reduction import AbstractReducer
from pickle import TRUE
from projects.models import Task
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User, AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models

#now create a team model