from django import forms


class CalculateSumForm(forms.Form):
    start = forms.DateTimeField(input_formats=["%d.%m.%Y %H:%M"])
    end = forms.DateTimeField(input_formats=["%d.%m.%Y %H:%M"])


class CreateNewEventForm(forms.Form):
    title = forms.CharField(max_length=50)
    date_of_the_event = forms.DateTimeField(input_formats=["%d.%m.%Y %H:%M", "%d.%m.%Y %H:%M:%S"])
    comment = forms.CharField(max_length=100)
    price = forms.IntegerField(min_value=0)