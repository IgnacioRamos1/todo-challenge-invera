from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    complete = models.BooleanField(default=False)
    expiration_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title
