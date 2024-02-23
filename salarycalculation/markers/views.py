from django.shortcuts import redirect, render
from .forms import CreateNewMarkerForm
from django.contrib.auth.decorators import login_required
from .models import Marker


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
    markers = request.user.markers.all()
    return render(request, 'markers/list.html', {'markers': markers, 'form': form})


@login_required
def markers_detail(request, marker_id):
    marker = Marker.objects.get(id=marker_id)
    return render(request, 'markers/marker_detail.html', {'marker': marker})