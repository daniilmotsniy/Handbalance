from django.db import models

# Create your models here.


class Post(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=512)
    content = models.CharField(max_length=64)

    def __str__(self):
        return "Title: " + str(self.name) + ", description: " + str(self.description) + \
               ", is about: " + str(self.content)