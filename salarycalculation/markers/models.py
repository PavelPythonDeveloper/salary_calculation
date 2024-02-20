from django.db import models
from django.contrib.auth.models import User


class Marker(models.Model):
    name = models.CharField(max_length=50, unique=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='markers', default=None)
