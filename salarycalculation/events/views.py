from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Event


def events_list(request):
    events = Event.objects.all()
    empty_event_list_msg = 'You have no event. Add one?'
    return render(request, 'events/event/list.html',
                  {'events': events,
                   'empty_event_list_msg': empty_event_list_msg})


def events_detail(request, id):
    event = get_object_or_404(Event, id=id)
    return render(request, 'events/event/detail.html', {'event': event})
