from django.db import models
from django.contrib.auth.models import User


class Marker(models.Model):
    name = models.CharField(max_length=50)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='markers', default=None)

    def __str__(self):
        return f"{self.name}, {self.creator}"
