from django.conf import settings
from django.db import models


class Notification(models.Model):
    class NotificationType(models.TextChoices):
        COMMENT = "comment", "Comment"
        STATUS_CHANGE = "status_change", "Status Change"
        NEW_VULNERABILITY = "new_vulnerability", "New Vulnerability"
        CRITICAL_ALERT = "critical_alert", "Critical Alert"

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    actor = models.ForeignKey( # sender
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="created_notifications",
        null=True,
        blank=True
    )

    type = models.CharField(
        max_length=50,
        choices=NotificationType.choices
    )

    title = models.CharField(max_length=200)
    message = models.TextField()
    url = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title