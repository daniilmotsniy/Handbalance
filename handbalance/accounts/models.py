from django.db import models
from django.contrib.auth.models import User


class TaskList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tasks = models.PositiveIntegerField()
    balance = models.IntegerField(max_length=140, default=0)
