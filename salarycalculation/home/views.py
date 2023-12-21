from django.shortcuts import render, redirect


def index(request):
    if request.user.is_authenticated:
        return redirect('events:events_list')
    return render(request, 'index.html')
