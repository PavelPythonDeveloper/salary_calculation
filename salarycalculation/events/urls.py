from django.urls import path

from . import views

app_name = 'events'

urlpatterns = [
    path('list/', views.events_list, name="events_list"),
    path('list/filter/<str:marker_id>/', views.events_list, name="events_list"),
    path('calculate/', views.calculate, name='calculate'),
    path('create/', views.create_new_event, name='create'),
    path('delete/<int:id>/', views.delete_event, name='delete'),
    path('update/<int:id>/', views.update_event, name='update'),
    path('list/filter/', views.marker_filter, name='marker_filter')
]
