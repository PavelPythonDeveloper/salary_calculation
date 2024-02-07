from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required


@login_required
def marker_filter(request):
    marker_id = request.POST.get('filter')
    if marker_id == 'None':
        return redirect('events:events_list')
    return redirect('events:events_list', marker_id=marker_id)
