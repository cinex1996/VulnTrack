from django.contrib.auth import get_user_model
from django.test import TestCase

from accounts.forms import RegisterForm
from accounts.models import VulnTrackAccounts


# Create your tests here.
class AccountsModelTest(TestCase):
    def test_Researcher(self):
        User = get_user_model()
        researcher = User.objects.create_user(username='test', password='test123')
        self.assertEqual(researcher.role, VulnTrackAccounts.Roles.RESEARCHER)

    def test_register_view_get(self):
        User = get_user_model()
        user = User.objects.create_user(username='test', password='test123', email='test123@gmail.com')
        self.client.login(username='test', password='test123')
        response = self.client.get('/accounts/register/')
        self.assertEqual(response.status_code, 200)

    def test_register_view_post(self):
        User = get_user_model()
        user = User.objects.create_user(username='test', password='test123', email='test123@gmail.com')
        self.client.login(username='test', password='test123')
        response = self.client.post('/accounts/register/',{
            'username':'newuser','email':'test@onet.pl','password1':'test@1!2','password2':'test@1!2'
        })
        self.assertRedirects(response, '/vulnerabilities/')

    def test_login_view_get(self):
        User = get_user_model()
        user = User.objects.create_user(username='test', password='test123')
        self.client.login(username='test', password='test123')
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)