from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class TaskList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tasks = models.PositiveIntegerField()
    balance = models.IntegerField(default=0)
    last_activity = models.DateField(default=timezone.now)
