from django.conf import settings

from VulnTrackAdmin.settings import AUTH_USER_MODEL
from notifications.models import Notification

def custom_notification(request):
    if request.user.is_authenticated:
        count = Notification.objects.filter(
            recipient=request.user,
            is_read=False
        ).count()
        recent_notifications = Notification.objects.filter(
            recipient=request.user
        )[:5]
        return {
            'unread_notifications_count': count,
            'recent_notifications': recent_notifications,
        }

    return {
        'unread_notifications_count': 0,
        'recent_notifications': [],
    }
