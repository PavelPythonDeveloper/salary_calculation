from django.urls import path

from . import views

app_name = 'events'

urlpatterns = [
    path('list/', views.events_list, name="events_list"),
    path('detail/<int:id>/', views.events_detail, name="events_detail"),
    path('calculate/', views.calculate, name='calculate'),
    path('create/', views.create_new_event, name='create')
]
