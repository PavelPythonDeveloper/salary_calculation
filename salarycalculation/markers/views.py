from django.shortcuts import redirect, render, HttpResponseRedirect, reverse, HttpResponse
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
    context = {}
    if request.method == 'POST':
        form = CreateNewMarkerForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            m = Marker(creator=request.user, name=name)
            m.save()
            return redirect('markers:markers_list')
    form = CreateNewMarkerForm()
    if request.GET.get('for_event'):
        event = Event.objects.get(id=request.GET.get('for_event'))
        context.update(event=event)
    markers = request.user.markers.all()
    context.update(markers=markers, form=form)
    return render(request, 'markers/list.html', context)


@login_required
def add_marker_to_event(request, event_id):
    if request.method == 'POST':
        choices = request.POST.getlist('choice')
        if event_id != 'None':
            event = Event.objects.get(id=int(event_id))
            for marker in request.user.markers.all():
                if str(marker.id) not in choices:
                    event.markers.remove(marker)
                else:
                    event.markers.add(marker)

        page = request.GET.get('event_page', 1)
        return HttpResponseRedirect(reverse('events:events_list') + f'?page={page}')


@login_required
def remove_marker(request, marker_id):
    if request.method == 'POST':
        marker = Marker.objects.get(id=marker_id)
        marker.delete()
        return HttpResponse('marker removed!!!')


@login_required
def markers_detail(request, marker_id):
    marker = Marker.objects.get(id=marker_id)
    return render(request, 'markers/marker_detail.html', {'marker': marker})
