from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register, name="register"),
    path('login/', views.LoginFormView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('username-change/', views.username_change, name='username_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password-change/', auth_views.PasswordChangeView.as_view(success_url=reverse_lazy('users:password_change_done')), name='password_change'),
    
]
