from django import forms


class CreateNewMarkerForm(forms.Form):
    name = forms.CharField(max_length=50, help_text='Create new marker')
