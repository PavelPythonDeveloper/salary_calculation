from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.admin.widgets import AdminDateWidget


# class CustomAdminDateWidget(forms.DateInput):
#     class Media:
#         js = ("/admin/jsi18n/",
#               "/static/admin/js/vendor/jquery/jquery.js",
#               "/static/admin/js/calendar.js",
#               "/static/admin/js/jquery.init.js",
#               "/static/admin/js/admin/DateTimeShortcuts.js",
#               "/static/admin/js/core.js")
#
#     def __init__(self, attrs=None, format=None):
#         attrs = {'class': 'vDateField', 'size': '10', **(attrs or {})}
#         super().__init__(attrs=attrs, format=format)


class CalculateSumForm(forms.Form):
    start_date = forms.DateField(label=_('start date'), input_formats=["%d.%m.%Y"])
    start_time = forms.TimeField(label=_('start time'), input_formats=["%H:%M"])
    end_date = forms.DateField(label=_('end date'), input_formats=["%d.%m.%Y"])
    end_time = forms.TimeField(label=_('end time'), input_formats=["%H:%M"])


class CreateNewEventForm(forms.Form):
    title = forms.CharField(label=_('title'), max_length=50)
    date_of_the_event = forms.DateField(widget=AdminDateWidget, label=_('date of the event'),
                                        input_formats=["%d.%m.%Y", "%Y-%m-%d"])
    time_of_the_event = forms.TimeField(label=_('time of the event'), input_formats=["%H:%M:%S", '%H:%M'])
    comment = forms.CharField(label=_('comment'), max_length=100, required=False)
    paid = forms.BooleanField(label=_('paid'), required=False)
    price = forms.IntegerField(label=_('price'), min_value=0)
