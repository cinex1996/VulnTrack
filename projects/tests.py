from django.test import TestCase
from django.contrib.auth import get_user_model
from projects.models import Project

class ProjectModelTest(TestCase):
    def test_str(self):
        project = Project(name="Test")
        self.assertEqual(str(project), "Test")

    def test_is_active_default(self):
        project = Project(name="Test")
        self.assertTrue(project.is_active)

    def test_project_list_requirements_login(self):
        response = self.client.get('/projects/')
        self.assertEqual(response.status_code, 302)

    def test_project_list_logged_in(self):
        User = get_user_model()
        user = User.objects.create_user(username='tester', password='pass1234')
        self.client.login(username='tester', password='pass1234')
        response = self.client.get('/projects/')
        self.assertEqual(response.status_code, 200)