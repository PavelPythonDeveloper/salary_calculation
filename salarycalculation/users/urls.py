from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register, name="register"),
    path('login/', views.LoginFormView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout')
]
