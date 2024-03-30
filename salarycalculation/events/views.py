from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Event, Marker
from django.contrib.auth.decorators import login_required
from .forms import CalculateSumForm, CreateNewEventForm
from django.contrib import messages
from django.core.paginator import Paginator
import datetime
from utils.customcalendar import custom_calendar
from django.utils.timezone import make_aware, get_current_timezone
from django.utils import timezone
from django.utils.translation import gettext as _
from django.utils.safestring import mark_safe


@login_required
def events_list(request):
    user = request.user

    clndr = custom_calendar.CustomHTMLCal(firstweekday=0)
    year = request.GET.get('year', None)
    theyear = request.GET.get('year', None)
    themonth = request.GET.get('month', None)
    theday = request.GET.get('day', None)
    if theday and themonth and theyear:
        thedate = datetime.date(year=int(theyear), month=int(themonth), day=int(theday))
        print(thedate)
        events = Event.objects.filter(creator=user, date_of_the_event=thedate)
        print(events)
    events = Event.objects.filter(creator=user, date_of_the_event__year=year)

    if year:
        c = mark_safe(clndr.formatyear(int(year), events=events))
    else:
        c = mark_safe(clndr.formatyear(timezone.now().year, events=events))

    return render(request, 'events/calendar.html', {"c": c})
    f = request.GET.get('f', None)
    if f != 'Default' and f is not None:
        events = Event.objects.filter(creator=request.user, markers__name=f)
    else:
        events = Event.objects.filter(creator=request.user)

    paginator = Paginator(events, 8)
    page_range = paginator.page_range
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, 'events/list.html',
                  {'events': events,
                   'user_id': request.user.id,
                   "page_obj": page_obj,
                   "page_range": page_range,
                   "cln": cln}
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
            return HttpResponse(_('You have no events in this period'))
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

            date_time_of_the_event = make_aware(datetime.datetime.combine(date_of_the_event, time_of_the_event))

            price = form.cleaned_data['price']
            creator = request.user
            event = Event(title=title,
                          comment=comment,
                          date_of_the_event=date_time_of_the_event,
                          price=price, creator=creator)
            event.save()

            messages.success(request, _("You have been created new event!"))
            return redirect('events:events_list')
        return render(request, 'events/create.html', {'form': form})

    form = CreateNewEventForm()
    return render(request, 'events/create.html', {'form': form})


@login_required
def delete_event(request, id):
    event = get_object_or_404(Event, id=id)
    if request.method == 'POST':
        event.delete()
        messages.success(request, _("You have been deleted the event!"))
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
            time_of_the_event = form.cleaned_data['time_of_the_event']
            date_time = make_aware(datetime.datetime.combine(date_of_the_event, time_of_the_event))
            event.date_of_the_event = date_time
            event.save()

            messages.success(request, _("You have been updated the event!"))

            return redirect('events:events_list')
    current_timezone = get_current_timezone()
    datetimes = event.date_of_the_event.astimezone(current_timezone)
    date = datetimes.date()
    times = datetimes.time()
    data = {'date_of_the_event': date.strftime('%d.%m.%Y'),
            'time_of_the_event': times.strftime('%H:%M'),
            'price': event.price,
            'comment': event.comment,
            'title': event.title}
    form = CreateNewEventForm(data)
    return render(request, 'events/create.html', {'form': form, 'id': event.id, 'action_flag': 'update'})
