from django.db import models
from markers.models import Marker
from django.utils import timezone
from django.contrib.auth.models import User


class Preset(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='preset', default=None)
    title = models.CharField(max_length=200)
    comment = models.CharField(max_length=200)
    time_of_the_event = models.TimeField(default=timezone.now)
    price = models.IntegerField(default=0)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='presets', default=None)
    markers = models.ManyToManyField(Marker, related_name='presets', default=None)