from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.utils.translation import gettext_lazy as _


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class UserLoginForm(forms.Form):
    username = forms.CharField(label=_('username'), max_length=50)
    password = forms.CharField(label=_('password'), max_length=50)


class UsernameChangeForm(forms.Form):
    username = forms.CharField(label=_('username'), max_length=50)
