from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            context = {'new_user': new_user}
            return render(request, 'users/register_done.html', context=context)
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

