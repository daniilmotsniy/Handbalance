from django.contrib import admin
from . import models

admin.site.register(models.TaskList)
admin.site.register(models.TaskBlock)
