from django.urls import path
from notifications import views

urlpatterns = [
    path('', views.notification_view, name='notifications'),
    path('<int:pk>/read/', views.mark_as_read, name="notification_read"),
    path('mark-all-read/', views.mark_all_as_read, name="mark_all_as_read"),
]
