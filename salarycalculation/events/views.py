from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Event


def events_list(request):
    events = Event.objects.all()
    print(events)
    return render(request, 'events/event/list.html', {'events': events})