from django.shortcuts import redirect, render, HttpResponseRedirect, reverse, HttpResponse
from .forms import CreateNewMarkerForm
from django.contrib.auth.decorators import login_required
from .models import Marker
from events.models import Event
from django.contrib import messages
from django.utils.translation import gettext as _
from django.utils.translation import activate


@login_required
def markers_list(request):
    activate('en')
    context = {}
    if request.method == 'POST':
        form = CreateNewMarkerForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            m = Marker(creator=request.user, name=name)
            m.save()
            messages.success(request, _("You have benn successfully added marker"))
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

            messages.success(request, _("You have been successfully changed the markers of event %(names)s") % {
                'names': event.title})

        page = request.GET.get('event_page', 1)
        return HttpResponseRedirect(reverse('events:events_list') + f'?page={page}')


@login_required
def remove_marker(request, marker_id):
    if request.method == 'POST':
        marker = Marker.objects.get(id=marker_id)
        marker.delete()
        messages.success(request, _("You have been successfully removed marker %(name)s") % {"name": marker.name})
        return HttpResponseRedirect(reverse('markers:markers_list'))
