from django.urls import path, include
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('reset/', views.password_reset_view, name ='password_reset'),
    path('', include('django.contrib.auth.urls')),
]