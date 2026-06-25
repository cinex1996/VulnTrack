from django.contrib.auth import get_user_model
from django.test import TestCase
from .factories import UserFactory
from accounts.forms import RegisterForm
from accounts.models import VulnTrackAccounts


# Create your tests here.
class AccountsModelTest(TestCase):
    def test_create_researcher(self):
        account = UserFactory()
        self.assertEqual(account.role, account.Roles.RESEARCHER)

    def test_register_view_get(self):
        account = UserFactory()
        self.client.login(username=account.username, password=account.password)
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
        account = UserFactory()
        self.client.login(username=account.email, password=account.password)
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)