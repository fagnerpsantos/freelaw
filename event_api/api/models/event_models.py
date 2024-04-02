from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)


    def __str__(self):
        return self.name
