from django.db import models
from django.conf import settings
from projects.models import Project

# Create your models here.
class Vulnerability(models.Model):
    class Status(models.TextChoices):
        open = 'open', "OPEN"
        new = 'new','NEW'
        triaged = 'triaged','TRIAGED'
        accepted = 'accepted','ACCEPTED'
        rejected = 'rejected','REJECTED'
        fixed = 'fixed','FIXED'
        closed = 'closed','CLOSED'

    class Severity(models.TextChoices):
        low = 'low','LOW'
        medium = 'medium','MEDIUM'
        high = 'high','HIGH'
        critical = 'critical','CRITICAL'

    title = models.CharField(max_length=200)
    description = models.TextField()
    severity = models.CharField(max_length=20, choices=Severity, default=Severity.low)
    status = models.CharField(max_length=20,choices=Status, default=Status.new)
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Comment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    vulnerability = models.ForeignKey(Vulnerability, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

class History(models.Model):
    vulnerability = models.ForeignKey(Vulnerability, on_delete=models.CASCADE, related_name="history")
    old_status = models.CharField(max_length=20, choices=Vulnerability.Status.choices)
    new_status = models.CharField(max_length=20, choices=Vulnerability.Status.choices)
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.vulnerability.title}: {self.old_status} -> {self.new_status} by {self.changed_by}"
