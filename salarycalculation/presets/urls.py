from django.urls import path
from . import views

app_name = "presets"


urlpatterns = [
    path('create_preset/', views.create_preset, name='create_preset'),
]