from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views


app_name = 'users'

urlpatterns = [
    path('register/', views.register, name="register"),
    path('login/', views.LoginFormView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('username-change/', views.username_change, name='username_change'),
    path('password-change/', views.PasswordChangeCustomView.as_view(success_url=reverse_lazy('users:profile'), template_name='registration/password_change.html'), 
                                                                   name='password_change'),
]
