
from django.test import TestCase
from django.urls import reverse

from accounts.factories import UserFactory
from notifications.models import Notification
from projects.models import Project
from vulnerabilities.models import Vulnerability, Comment

# Create your tests here.
class CommentCreatesNotification(TestCase):
    def test_comment_creates_notification(self):
        reporter = UserFactory()
        project = Project.objects.create(name="title", description="title")
        vulln = Vulnerability.objects.create(reporter=reporter, title="title", project=project)
        user = UserFactory()
        self.client.force_login(user)
        response = self.client.post(reverse("vulnerability_detail", kwargs={"id": vulln.id}),
                                    {'comment_submit':'true','content':'Test content'})
        notification = Notification.objects.get(recipient=reporter)
        self.assertTrue(Comment.objects.filter(author=user, vulnerability=vulln).exists())
        self.assertTrue(Notification.objects.filter(recipient=reporter).exists())
        self.assertEqual(notification.type, 'comment')

class NotificationModelTest(TestCase):
    def test_str(self):
        user = UserFactory()
        notification = Notification.objects.create(recipient=user,title="title")
        self.assertEqual(str(notification), notification.title)

    def test_is_read(self):
        user = UserFactory()
        notification = Notification.objects.create(recipient=user, title="title")
        self.assertFalse(notification.is_read)

    def test_not_notification_view(self):
        user = UserFactory()
        self.client.force_login(user)
        response = self.client.get('/notifications/')
        self.assertEqual(response.context['no_notifications_message'],"Nie ma żadnych powiadomień")

    def test_notification_view(self):
        user = UserFactory()
        self.client.force_login(user)
        notification = Notification.objects.create(recipient=user, title="title")
        response = self.client.get('/notifications/')
        self.assertIn(notification,response.context['notifications'])

    def test_notification_mark_as_read(self):
        user = UserFactory()
        self.client.force_login(user)
        notification = Notification.objects.create(recipient=user, title="title")
        response = self.client.post(f'/notifications/{notification.id}/read/')
        notification.refresh_from_db()
        self.assertRedirects(response,'/notifications/')
        self.assertTrue(notification.is_read)

    def test_notification_mark_as_not_read(self):
        owner = UserFactory()
        other = UserFactory()
        notification = Notification.objects.create(recipient=owner, title="title")
        self.client.force_login(other)
        response = self.client.post(f'/notifications/{notification.id}/read/')
        notification.refresh_from_db()
        self.assertEqual(response.status_code, 404)
        self.assertFalse(notification.is_read)