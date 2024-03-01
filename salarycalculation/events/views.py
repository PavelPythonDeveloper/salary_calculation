import zoneinfo

from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from .models import Event, Marker
from django.contrib.auth.decorators import login_required
from .forms import CalculateSumForm, CreateNewEventForm
from django.contrib import messages
from django.core.paginator import Paginator
import datetime
from django.utils.timezone import make_aware, tzinfo, is_aware, is_naive, utc, get_current_timezone


@login_required
def events_list(request):
    f = request.GET.get('f', None)
    if f != 'Default' and f is not None:
        events = Event.objects.filter(creator=request.user, markers__name=f)
    else:
        events = Event.objects.filter(creator=request.user)

    empty_event_list_msg = 'You have no event. Add one?'
    paginator = Paginator(events, 8)
    page_range = paginator.page_range
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, 'events/list.html',
                  {'events': events,
                   'empty_event_list_msg': empty_event_list_msg,
                   'user_id': request.user.id,
                   "page_obj": page_obj,
                   "page_range": page_range}
                  )


@login_required
def calculate(request):
    if request.method == 'POST':
        form = CalculateSumForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            start_time = form.cleaned_data['start_time']

            end_date = form.cleaned_data['end_date']
            end_time = form.cleaned_data['end_time']

            start = datetime.datetime.combine(start_date, start_time)
            end = datetime.datetime.combine(end_date, end_time)
            events = Event.objects.filter(date_of_the_event__gte=start).filter(date_of_the_event__lte=end)
            if events:
                amount = 0
                for event in events:
                    amount += event.price
                return render(request, 'events/calculate.html', {'amount': amount,
                                                                 'start': start,
                                                                 'end': end, 'form': form})
            return HttpResponse('You have no events in this period')
    form = CalculateSumForm()
    return render(request, 'events/calculate.html', {'form': form})


@login_required
def create_new_event(request):
    if request.method == 'POST':
        form = CreateNewEventForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            comment = form.cleaned_data['comment']
            date_of_the_event = form.cleaned_data['date_of_the_event']
            time_of_the_event = form.cleaned_data['time_of_the_event']

            date_time_of_the_event = make_aware(datetime.datetime.combine(date_of_the_event, time_of_the_event),
                                                timezone=request.session.get('django-timezone'))
            print('datetime is aware', is_aware(date_time_of_the_event))
            price = form.cleaned_data['price']
            creator = request.user
            event = Event(title=title,
                          comment=comment,
                          date_of_the_event=date_time_of_the_event,
                          price=price, creator=creator)
            event.save()
            print('is aware!', is_aware(event.date_of_the_event))
            messages.success(request, "You have been created new event!")
            return redirect('events:events_list')
        return render(request, 'events/create.html', {'form': form})

    form = CreateNewEventForm()
    return render(request, 'events/create.html', {'form': form})


@login_required
def delete_event(request, id):
    event = get_object_or_404(Event, id=id)
    if request.method == 'POST':
        event.delete()
        messages.success(request, "You have been deleted the event!")
        return redirect('events:events_list')
    return render(request, 'events/delete_confirmation.html', {'event_id': event.id})


@login_required
def update_event(request, id):
    event = get_object_or_404(Event, id=id)
    if event.creator != request.user:
        return HttpResponse("You can't see it!")
    if request.method == 'POST':
        form = CreateNewEventForm(request.POST)
        if form.is_valid():
            event.title = form.cleaned_data['title']
            event.comment = form.cleaned_data['comment']
            event.price = form.cleaned_data['price']
            date_of_the_event = form.cleaned_data['date_of_the_event']
            # print(is_aware(date_of_the_event))
            time_of_the_event = form.cleaned_data['time_of_the_event']
            date_time = make_aware(datetime.datetime.combine(date_of_the_event, time_of_the_event),
                                   timezone=request.session.get('django_timezone'))
            aware = date_time
            event.date_of_the_event = aware
            event.save()

            messages.success(request, "You have been updated the event!")

            return redirect('events:events_list')
    localdate = zoneinfo.ZoneInfo('Europe/Moscow')
    datetimes = event.date_of_the_event.astimezone(localdate)
    date = datetimes.date()
    times = datetimes.time()
    data = {'date_of_the_event': date.strftime('%d.%m.%Y'),
            'time_of_the_event': times.strftime('%H:%M'),
            'price': event.price,
            'comment': event.comment,
            'title': event.title}
    form = CreateNewEventForm(data)
    return render(request, 'events/create.html', {'form': form, 'id': event.id, 'action': 'update'})
