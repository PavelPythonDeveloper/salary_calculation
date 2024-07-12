from django import forms
from django.forms.widgets import SelectMultiple, CheckboxSelectMultiple
from markers.models import Marker


class CreateNewPresetForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(CreateNewPresetForm, self).__init__(*args, **kwargs)
        self.fields['markers'].queryset = Marker.objects.filter(creator=self.user)

    title = forms.CharField(max_length=200)
    comment = forms.CharField(max_length=200)
    time_of_the_event = forms.TimeField()
    price = forms.IntegerField()
    markers = forms.ModelMultipleChoiceField(widget=SelectMultiple, queryset=None)

