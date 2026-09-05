from django.contrib.auth import get_user_model

from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from accounts.models import VulnTrackAccounts


@shared_task
def send_password_reset_email(user_id,token):
    try:
        user = VulnTrackAccounts.objects.get(id=user_id)
    except VulnTrackAccounts.DoesNotExist:
        return f"User with id {user_id} does not exist"
    reset_url = f"{settings.SITE_URL}/accounts/reset/{token}"
    message = (
        f"Hi {user.username},\n\n"
        f"Click the link below to reset your password:\n"
        f"{reset_url}"
    )
    send_mail(
        subject='Password reset',
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
    )
