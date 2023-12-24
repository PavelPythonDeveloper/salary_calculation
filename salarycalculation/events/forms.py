from django import forms


class DateInput(forms.DateInput):
    input_type = 'date'


class TimeInput(forms.TimeInput):
    input_type = 'time'


class CalculateSumForm(forms.Form):
    start_date = forms.DateTimeField(input_formats=["%d.%m.%Y"], widget=DateInput)
    start_time = forms.TimeField(input_formats=["%H:%M"], widget=TimeInput)
    end_date = forms.DateTimeField(input_formats=["%d.%m.%Y"], widget=DateInput)
    end_time = forms.TimeField(input_formats=["%H:%M"], widget=TimeInput)


class CreateNewEventForm(forms.Form):
    title = forms.CharField(max_length=50)
    date_of_the_event = forms.DateTimeField(input_formats=["%d.%m.%Y"], widget=DateInput)
    time_of_the_event = forms.TimeField(input_formats=["%H:%M"], widget=TimeInput)
    comment = forms.CharField(max_length=100)
    price = forms.IntegerField(min_value=0)
