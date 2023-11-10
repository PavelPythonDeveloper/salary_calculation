from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Event
from django.contrib.auth.decorators import login_required


@login_required()
def events_list(request, user_id):
    events = Event.objects.all()
    empty_event_list_msg = 'You have no event. Add one?'
    return render(request, 'events/event/list.html',
                  {'events': events,
                   'empty_event_list_msg': empty_event_list_msg,
                   'user_id': user_id},
                  )


@login_required()
def events_detail(request, id):
    event = get_object_or_404(Event, id=id)
    return render(request, 'events/event/detail.html', {'event': event})
