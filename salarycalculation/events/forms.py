from django import forms
from django.utils.translation import gettext_lazy as _


class CalculateSumForm(forms.Form):
    start_date = forms.DateField(label=_('start date'), input_formats=["%d.%m.%Y"])
    start_time = forms.TimeField(label=_('start time'), input_formats=["%H:%M"])
    end_date = forms.DateField(label=_('end date'), input_formats=["%d.%m.%Y"])
    end_time = forms.TimeField(label=_('end time'), input_formats=["%H:%M"])


class CreateNewEventForm(forms.Form):
    title = forms.CharField(label=_('title'), max_length=50)
    date_of_the_event = forms.DateField(label=_('date of the event'), input_formats=["%d.%m.%Y", "%Y-%m-%d"])
    time_of_the_event = forms.TimeField(label=_('time of the event'), input_formats=["%H:%M:%S", '%H:%M'])
    comment = forms.CharField(label=_('comment'), max_length=100, required=False)
    price = forms.IntegerField(label=_('price'), min_value=0)
