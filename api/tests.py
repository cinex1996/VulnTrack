from django.template.defaultfilters import title

from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from django.urls import reverse
from vulnerabilities.models import Vulnerability
from projects.models import Project
from accounts.factories import UserFactory

class testVulnerability(APITestCase):
    def test_vulnerabilities_list(self):
        user = UserFactory()
        project = Project.objects.create(name="Test Project", description="Test description")
        vuln=Vulnerability.objects.create(title="Test Vuln",
                                          reporter=user,
                                          project=project)
        response = self.client.get(reverse("vulnerability-list"))
        self.assertEqual(response.status_code,200)
        self.assertIn('title',response.data[0])

    def test_vulnerability_latest(self):
        user = UserFactory()
        project = Project.objects.create(name="Test Project", description="Test description")
        vuln=Vulnerability.objects.create(title="Test Vuln", reporter=user, project=project)
        response = self.client.get(reverse("vulnerability-latest"))
        self.assertEqual(response.status_code,200)
        self.assertIn("title",response.data[0])

    def test_projects_list(self):
        project = Project.objects.create(name="Test Project", description="Test")

        response = self.client.get(reverse("project-list"))

        self.assertEqual(response.status_code, 200)
        self.assertIn('name', response.data[0])