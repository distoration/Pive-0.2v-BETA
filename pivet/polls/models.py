from django.db import models

class Task(models.Model):
    id = models.AutoField(primary_key=True)
    number = models.IntegerField()
    description = models.CharField(max_length=255)
    notes = models.TextField()
    in_progress = models.BooleanField(default=False)
    paused = models.BooleanField(default=False)
    done = models.BooleanField(default=False)
    date = models.DateField()
    time_elapsed = models.IntegerField(default=0)
    time_spent = models.IntegerField(default=0)
    uuid = models.CharField(max_length=255)
