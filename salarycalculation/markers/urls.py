from django.urls import path

from . import views

app_name = "markers"


urlpatterns = [
    # path('create/', views.create_marker, name='create_marker'),
    path('add_marker_to_event/<str:event_id>', views.add_marker_to_event, name='add_marker_to_event'),
    path('remove/<int:marker_id>', views.remove_marker, name='remove'),
    path('list/', views.markers_list, name='markers_list'),
]
