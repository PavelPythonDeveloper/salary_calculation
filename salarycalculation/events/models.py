import datetime

from django.db import models
from django.contrib.auth.models import User
from markers.models import Marker
from django.utils import timezone


class Event(models.Model):
    title = models.CharField(max_length=200)
    comment = models.CharField(max_length=200)
    date_of_creation = models.DateTimeField(default=timezone.now)
    date_of_the_event = models.DateTimeField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events', default=None)
    price = models.IntegerField(default=0)
    markers = models.ManyToManyField(Marker)

    def in_future(self):
        if self.date_of_the_event > timezone.now() + timezone.timedelta(1):
            print(timezone.now())
            return True
        return False

    def in_past(self):
        if self.date_of_the_event < timezone.now():
            return True
        return False

    def today(self):
        if timezone.now() < self.date_of_the_event < timezone.now() + timezone.timedelta(1):
            return True
        return False

    class Meta:
        ordering = ['-date_of_the_event']

    def __str__(self):
        return self.title
