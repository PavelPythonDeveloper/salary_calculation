from django import forms
from django.utils.translation import gettext_lazy as _


class CreateNewMarkerForm(forms.Form):
    name = forms.CharField(label=_(''), max_length=50, help_text='Create new marker')
