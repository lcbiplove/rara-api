from django.urls import path
from core import views

urlpatterns = [
    path('api/auth/login/', views.LoginView.as_view(), name='login'),
    path('api/me/', views.UserProfileView.as_view(), name='profile'),
]
