from django.test import TestCase
from django.urls import reverse

from accounts.models import VulnTrackAccounts


class RegisterViewTest(TestCase):
    def test_register_creates_user_and_redirects(self):
        response = self.client.post(reverse('register'), {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        })
        self.assertRedirects(response, reverse('index'))
        self.assertTrue(VulnTrackAccounts.objects.filter(username='testuser').exists())

    def test_register_with_mismatched_passwords_fails(self):
        response = self.client.post(reverse('register'), {
            'username': 'testuser2',
            'email': 'test2@example.com',
            'password1': 'StrongPass123!',
            'password2': 'WrongPass999!',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(VulnTrackAccounts.objects.filter(username='testuser2').exists())


class LoginViewTest(TestCase):
    def setUp(self):
        self.user = VulnTrackAccounts.objects.create_user(
            username='loginuser', password='TestPass123!'
        )

    def test_correct_credentials_redirect_to_index(self):
        response = self.client.post(reverse('login'), {
            'username': 'loginuser',
            'password': 'TestPass123!',
        })
        self.assertRedirects(response, reverse('index'))

    def test_wrong_password_shows_error(self):
        response = self.client.post(reverse('login'), {
            'username': 'loginuser',
            'password': 'WrongPassword!',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nieprawidłowa')


class RolesTest(TestCase):
    def test_researcher_is_not_moderator(self):
        user = VulnTrackAccounts.objects.create_user(
            username='researcher', password='pass', role=VulnTrackAccounts.Roles.RESEARCHER
        )
        self.assertFalse(user.is_moderator)

    def test_moderator_is_moderator(self):
        user = VulnTrackAccounts.objects.create_user(
            username='moderator', password='pass', role=VulnTrackAccounts.Roles.MODERATOR
        )
        self.assertTrue(user.is_moderator)

    def test_admin_is_moderator(self):
        user = VulnTrackAccounts.objects.create_user(
            username='admin_user', password='pass', role=VulnTrackAccounts.Roles.ADMIN
        )
        self.assertTrue(user.is_moderator)
