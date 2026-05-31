from django.urls import path
from notifications import views

urlpatterns = [
    path('notifications/', views.notification_view, name='notifications'),
    path('notifications/<int:pk>/read/', views.mark_as_read, name="notification_read"),
]
