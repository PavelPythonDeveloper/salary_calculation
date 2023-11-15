from django.shortcuts import render, get_object_or_404, HttpResponse
from django.http import HttpResponse
from .models import Event
from django.contrib.auth.decorators import login_required


@login_required
def events_list(request):
    events = Event.objects.filter(creator=request.user)
    empty_event_list_msg = 'You have no event. Add one?'
    return render(request, 'events/event/list.html',
                  {'events': events,
                   'empty_event_list_msg': empty_event_list_msg,
                   'user_id': request.user.id},
                  )


@login_required
def events_detail(request, id):
    event = get_object_or_404(Event, id=id)
    if event.creator == request.user:
        return render(request, 'events/event/detail.html', {'event': event})
    return HttpResponse("You can't view other people's events")


@login_required
def calculate(request, start, end):
    events = Event.objects.filter(date_of_the_event__gte=start).filter(date_of_the_event__lte=end)
    if events:
        amount = 0
        for event in events:
            amount += event.price
        return render(request, 'events/event/calculated.html', {'amount': amount,
                                                                'start': start,
                                                                'end': end})
    return HttpResponse('You have no events in this period')