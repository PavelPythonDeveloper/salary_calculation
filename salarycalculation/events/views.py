from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from django.http import HttpResponse
from .models import Event
from django.contrib.auth.decorators import login_required
from .forms import CalculateSumForm, CreateNewEventForm
from django.forms.models import model_to_dict
from django.contrib import messages


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
def calculate(request):
    if request.method == 'POST':
        form = CalculateSumForm(request.POST)
        if form.is_valid():
            start = form.cleaned_data['start']
            end = form.cleaned_data['end']
            events = Event.objects.filter(date_of_the_event__gte=start).filter(date_of_the_event__lte=end)
            if events:
                amount = 0
                for event in events:
                    amount += event.price
                return render(request, 'events/event/calculate.html', {'amount': amount,
                                                                       'start': start,
                                                                       'end': end, 'form': form})
            return HttpResponse('You have no events in this period')
    form = CalculateSumForm()
    return render(request, 'events/event/calculate.html', {'form': form})


@login_required
def create_new_event(request):
    if request.method == 'POST':
        form = CreateNewEventForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            comment = form.cleaned_data['comment']
            date_of_the_event = form.cleaned_data['date_of_the_event']
            price = form.cleaned_data['price']
            creator = request.user
            event = Event(title=title,
                          comment=comment,
                          date_of_the_event=date_of_the_event,
                          price=price, creator=creator)
            event.save()
            messages.success(request, "You have been created new event!")
            return redirect('events:events_list')
    form = CreateNewEventForm()
    return render(request, 'events/event/create.html', {'form': form})


@login_required
def delete_event(request, id):
    event = get_object_or_404(Event, id=id)
    if event:
        event.delete()
        messages.success(request, "You have been deleted the event!")
    return redirect('events:events_list')


@login_required
def update_event(request, id):
    event = get_object_or_404(Event, id=id)
    if request.method == 'POST':
        form = CreateNewEventForm(request.POST)
        if form.is_valid():
            event.title = form.cleaned_data['title']
            event.comment = form.cleaned_data['comment']
            event.price = form.cleaned_data['price']
            event.date_of_the_event = form.cleaned_data['date_of_the_event']
            event.save()
            messages.success(request, "You have been updated the event!")
            return redirect('events:events_list')

    form = CreateNewEventForm(initial=model_to_dict(event))
    return render(request, 'events/event/create.html', {'form': form, 'id': event.id, 'action': 'update'})
