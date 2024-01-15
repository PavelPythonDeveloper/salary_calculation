from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from .forms import UserRegisterForm, UserLoginForm
from django.contrib.messages.views import SuccessMessageMixin


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            context = {'new_user': new_user}
            return render(request, 'registration/register_done.html', context=context)
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})


def profile(request):
    user = request.user


class LoginFormView(SuccessMessageMixin, LoginView):
    template_name = 'registration/login.html'
    success_url = '/success_url/'
    success_message = "You were successfully logged in."
