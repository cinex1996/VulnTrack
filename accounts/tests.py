from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .factories import UserFactory
from accounts.forms import RegisterForm
from accounts.models import VulnTrackAccounts


User = get_user_model()


# Create your tests here.
class AccountsModelTest(TestCase):
    def test_create_researcher(self):
        account = UserFactory()
        self.assertEqual(account.role, account.Roles.RESEARCHER)

    def test_register_view_get(self):
        account = UserFactory()
        self.client.force_login(account)
        response = self.client.get('/accounts/register/')
        self.assertEqual(response.status_code, 200)

    def test_register_view_post(self):
        User = get_user_model()

        response = self.client.post('/accounts/register/',{
            'username':f'new_user','email':f'new_user@example.com','password1':f'StrongPass123!',
            'password2':f'StrongPass123!'
        })
        self.assertRedirects(response, '/vulnerabilities/')
        self.assertTrue(User.objects.filter(username=f'new_user').exists())

    def test_login_view_get(self):
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)

    def test_login_redirect_when_authenticated(self):
        account = UserFactory()
        self.client.force_login(account)
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 302)

class AccountsViewTest(TestCase):

    def test_register_view_get(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("register_form", response.context)

    def test_register_post_valid(self):
        response = self.client.post(reverse("register"), {
            'email':'user123@wp.pl',
            'username':f'new_user',
            'password1':f'Qwerty12!',
            'password2':f'Qwerty12!',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username=f'new_user').exists())