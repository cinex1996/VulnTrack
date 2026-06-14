from django.contrib.auth import get_user_model
from django.test import TestCase

from accounts.models import VulnTrackAccounts
from notifications.models import Notification


# Create your tests here.
class NotificationModelTest(TestCase):
    def test_str(self):
        User = get_user_model()
        user = User.objects.create_user(username='test', password='pass1234')
        notification = Notification.objects.create(recipient=user,title="title")
        self.assertEqual(str(notification), notification.title)

    def test_is_read(self):
        User = get_user_model()
        user = User.objects.create_user(username='test', password='pass1234')
        notification = Notification.objects.create(recipient=user, title="title")
        self.assertFalse(notification.is_read)

    def test_not_notification_view(self):
        User = get_user_model()
        user = User.objects.create_user(username='test', password='test123')
        self.client.login(username='test', password='test123')
        response = self.client.get('/notifications/')
        self.assertEqual(response.context['no_notifications_message'],"Nie ma żadnych powiadomień")

    def test_notification_view(self):
        User = get_user_model()
        user = User.objects.create_user(username='test', password='test123')
        notification = Notification.objects.create(recipient=user, title="title")
        self.client.login(username='test', password='test123')
        response = self.client.get('/notifications/')
        self.assertIn(notification,response.context['notifications'])

    def test_notification_mark_as_read(self):
        User = get_user_model()
        user = User.objects.create_user(username='test', password='test123')
        notification = Notification.objects.create(recipient=user, title="title")
        self.client.login(username='test', password='test123')
        response = self.client.get(f'/notifications/{notification.id}/read/')
        notification.refresh_from_db()
        self.assertRedirects(response,'/notifications/')
        self.assertTrue(notification.is_read)

    def test_notification_mark_as_not_read(self):
        User = get_user_model()
        owner = User.objects.create_user(username='test', password='test123')
        other = User.objects.create_user(username='other', password='other123')
        notification = Notification.objects.create(recipient=owner, title="title")
        self.client.login(username='other', password='other123')
        response = self.client.get(f'/notifications/{notification.id}/read/')
        notification.refresh_from_db()
        self.assertEqual(response.status_code, 404)
        self.assertFalse(notification.is_read)