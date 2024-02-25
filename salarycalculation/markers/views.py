from django.shortcuts import redirect, render, HttpResponseRedirect, reverse
from .forms import CreateNewMarkerForm
from django.contrib.auth.decorators import login_required
from .models import Marker
from events.models import Event


# @login_required
# def create_marker(request):
#     form = CreateNewMarkerForm()
#     if request.method == 'POST':
#         name = form.cleaned_data('name')
#         m = Marker(name=name)
#         m.save()
#     markers = request.user.markers.all()
#     return render(request, 'markers/list.html', {'form': form, 'markers': markers})


@login_required
def markers_list(request):
    if request.method == 'POST':
        form = CreateNewMarkerForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            m = Marker(creator=request.user, name=name)
            m.save()
            return redirect('markers:markers_list')
    form = CreateNewMarkerForm()
    if request.GET.get('for-event'):
        print(request.GET.get('for-event'))
        event = Event.objects.get(id=request.GET.get('for-event'))

    markers = request.user.markers.all()
    return render(request, 'markers/list.html', {'markers': markers, 'form': form, 'event': event})


@login_required
def add_marker_to_event(request, event_id):

    if request.method == 'POST':
        choices = request.POST.getlist('choice')
        event = Event.objects.get(id=event_id)
        for choice in choices:
            marker = Marker.objects.get(id=choice)
            event.markers.add(marker)
        page = request.GET.get('event_page', 1)
        f = request.GET.get('f')
        return HttpResponseRedirect(reverse('events:events_list') + f'?page={page}&f={f}')


@login_required
def markers_detail(request, marker_id):
    marker = Marker.objects.get(id=marker_id)
    return render(request, 'markers/marker_detail.html', {'marker': marker})
