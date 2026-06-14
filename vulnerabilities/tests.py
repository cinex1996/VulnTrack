from django.contrib.auth import get_user_model
from django.test import TestCase

from projects.models import Project
from vulnerabilities.models import Vulnerability


class VulnerabilitiesTest(TestCase):

    def test_str(self):
        User = get_user_model()
        user = User.objects.create_user(username='test', password='pass1234')
        project = Project.objects.create(name='Test')
        vulnerability = Vulnerability.objects.create(title="Test bug", reporter=user, project=project)
        self.assertEqual(str(vulnerability), "Test bug")

    def test_default_status(self):
        User = get_user_model()
        user = User.objects.create_user(username='test', password='pass1234')
        project = Project.objects.create(name='Test')
        vulnerability = Vulnerability.objects.create(reporter=user, project=project)
        self.assertEqual(vulnerability.status, Vulnerability.Status.new)

    def test_create_vulnerability_ignores_status_field(self):
        User = get_user_model()
        user = User.objects.create_user(username='test', password='pass1234')
        self.client.login(username='test', password='pass1234')
        project = Project.objects.create(name='Test')
        self.client.post('/vulnerabilities/create/', {
            'title': 'windows',
            'description': 'windows vulnerabilities',
            'severity': 'low',
            'project': project.id,
            'status': 'fixed',
        })
        vulnerability = Vulnerability.objects.get(title='windows')
        self.assertEqual(vulnerability.status, Vulnerability.Status.new)
