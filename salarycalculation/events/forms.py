from django import forms
from django.core.exceptions import ValidationError
from django.core import validators


class DateInput(forms.DateInput):
    input_type = 'date'


class TimeInput(forms.TimeInput):
    input_type = 'time'


class CalculateSumForm(forms.Form):
    start_date = forms.DateField(input_formats=["%d.%m.%Y"])
    start_time = forms.TimeField(input_formats=["%H:%M"])
    end_date = forms.DateField(input_formats=["%d.%m.%Y"])
    end_time = forms.TimeField(input_formats=["%H:%M"])


class CreateNewEventForm(forms.Form):
    title = forms.CharField(max_length=50)
    date_of_the_event = forms.DateField(input_formats=["%d.%m.%Y"])
    time_of_the_event = forms.TimeField(input_formats=["%H:%M:%S", '%H:%M'])
    comment = forms.CharField(max_length=100, required=False)
    price = forms.IntegerField(min_value=0)
