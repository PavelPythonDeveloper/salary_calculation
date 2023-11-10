from django.urls import path

from . import views

app_name = 'events'

urlpatterns = [
    path('list/<int:user_id>/', views.events_list, name="events_list"),
    path('detail/<int:id>/', views.events_detail, name="events_detail"),
]
