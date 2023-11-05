from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Event(models.Model):
    title = models.CharField(max_length=200)
    comment = models.CharField(max_length=200)
    date_of_creation = models.DateTimeField('Date of creation')
    date_of_the_event = models.DateTimeField('Date of the event')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    price = models.IntegerField(default=0)

    class Meta:
        ordering = ['date_of_the_event']