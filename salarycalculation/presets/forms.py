from django import forms
from django.forms.widgets import SelectMultiple, CheckboxSelectMultiple
from markers.models import Marker


class CreateNewPresetForm(forms.Form):
    title = forms.CharField(max_length=200)
    comment = forms.CharField(max_length=200)
    time_of_the_event = forms.TimeField()
    price = forms.IntegerField()
    markers = forms.ModelMultipleChoiceField(widget=SelectMultiple, queryset=Marker.objects.none())
