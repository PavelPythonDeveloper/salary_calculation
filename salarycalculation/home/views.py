from django.shortcuts import render, redirect
from django.utils.translation import activate


def index(request):
    if request.user.is_authenticated:
        return redirect('events:events_list')
    return render(request, 'home/index.html')
