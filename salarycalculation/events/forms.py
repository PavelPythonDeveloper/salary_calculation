from django import forms


class CalculateSumForm(forms.Form):
    start = forms.DateTimeField(input_formats=["%d.%m.%Y %H:%M"])
    end = forms.DateTimeField(input_formats=["%d.%m.%Y %H:%M"])