from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, PasswordChangeView
from .forms import UserRegisterForm, UsernameChangeForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages


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


@login_required
def profile(request):
    user = request.user
    context = {'username': user.username}
    return render(request, 'registration/profile.html', context=context)

@login_required
def username_change(request):
    if request.method == 'POST':
        form = UsernameChangeForm(request.POST)
        if form.is_valid():
            request.user.username = form.cleaned_data['username']
            request.user.save()
            messages.success(request, "You have been changed your username!")
            return redirect('users:profile')
    else:
        form = UsernameChangeForm(data={'username': request.user.username})
    return render(request, 'registration/username_change.html', {'form': form})


class LoginFormView(SuccessMessageMixin, LoginView):
    template_name = 'registration/login.html'
    success_url = '/success_url/'
    success_message = "You were successfully logged in."

class PasswordChangeCustomView(SuccessMessageMixin, PasswordChangeView):
    success_message = 'You have been successfully changed your password!!!'
