from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Event(models.Model):
    title = models.CharField(max_length=200)
    comment = models.CharField(max_length=200)
    date_of_creation = models.DateTimeField(default=timezone.now)
    date_of_the_event = models.DateTimeField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events', default=None)
    price = models.IntegerField(default=0)

    class Meta:
        ordering = ['-date_of_the_event']

    def __str__(self):
        return self.title