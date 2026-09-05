from django.urls import path, include
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('reset/<uidb64>/<token>/', views.password_reset_confirmation_view, name ='password_reset_confirm'),
    path('', include('django.contrib.auth.urls')),
]