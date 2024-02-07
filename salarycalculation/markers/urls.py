from django.urls import path

from . import views

app_name = "markers"


urlpatterns = [
    path('filter/<int:marker_id>', views.marker_filter, name='filter'),
    path('filter/', views.marker_filter, name='filter')
]
