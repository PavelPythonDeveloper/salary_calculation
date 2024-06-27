from django.contrib import admin
from django.db import models
from .models import Event
from widgets import CustomDatePickerWidget

# admin.site.register(Event)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.DateField: {'widget': CustomDatePickerWidget}
    }
