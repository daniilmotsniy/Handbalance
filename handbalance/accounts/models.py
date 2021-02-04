from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class TaskList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.IntegerField(default=0)
    last_activity = models.DateField(default=timezone.now)


class TaskBlock(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    block_id = models.PositiveIntegerField()
    tasks = models.PositiveIntegerField()
    tasks_count = models.PositiveIntegerField()
