from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Root Redirect (/)
    path('', views.root_redirect, name='root'),
    
    # URL Authentication
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # URL Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
]