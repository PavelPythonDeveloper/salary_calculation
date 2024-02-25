from django.urls import path

from . import views

app_name = "markers"


urlpatterns = [
    # path('create/', views.create_marker, name='create_marker'),
    path('detail/<int:marker_id>/', views.markers_detail, name='markers_detail'),
    path('add_marker_to_event/<int:event_id>', views.add_marker_to_event, name='add_marker_to_event'),
    path('list/', views.markers_list, name='markers_list'),
]
