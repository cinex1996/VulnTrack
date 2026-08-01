from datetime import timedelta
from django.template.defaultfilters import title
from django.utils import timezone
from django.test import tag
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from django.urls import reverse
from vulnerabilities.models import Vulnerability
from projects.models import Project
from accounts.factories import UserFactory

class testVulnerability(APITestCase):
    def test_vulnerabilities_list(self):
        user = UserFactory()
        self.client.force_login(user)
        project = Project.objects.create(name="Test Project", description="Test description")
        vuln=Vulnerability.objects.create(title="Test Vuln",
                                          reporter=user,
                                          project=project)
        response = self.client.get(reverse("vulnerability-list"))
        self.assertEqual(response.status_code,200)
        self.assertIn('title',response.data['results'][0])

    def test_vulnerability_latest(self):
        user = UserFactory()
        self.client.force_login(user)
        project = Project.objects.create(name="Test Project", description="Test description")
        vuln=Vulnerability.objects.create(title="Test Vuln", reporter=user, project=project)
        response = self.client.get(reverse("vulnerability-latest"))
        self.assertEqual(response.status_code,200)
        self.assertIn("title",response.data[0])

    def test_projects_list(self):
        user = UserFactory()
        self.client.force_login(user)
        project = Project.objects.create(name="Test Project", description="Test")
        response = self.client.get(reverse("project-list"))

        self.assertEqual(response.status_code, 200)
        self.assertIn('name', response.data['results'][0])

    @tag('x')
    def test_get_vulnerability_created_at(self):
        user = UserFactory()
        self.client.force_login(user)
        project = Project.objects.create(name="Test Project", description="Test description")
        vuln=Vulnerability.objects.create(title="Test Vuln",created_at=timezone.now(),reporter=user,project=project)
        vuln_next = Vulnerability.objects.create(title="Test Vuln", created_at=timezone.now(),reporter=user,project=project)
        response = self.client.get(reverse("vulnerability-list"), {"ordering": "-created_at"})
        self.assertEqual(response.status_code,200)
        print(response.json())

    def test_not_signed_in_user(self):
        user = UserFactory()
        response = self.client.get(reverse("vulnerability-list"))
        self.assertEqual(response.status_code,403)

    def test_not_signed_in_Project(self):
        user = UserFactory()
        response = self.client.get(reverse("project-list"))
        self.assertEqual(response.status_code,403)

    def test_non_reporter_cannot_update_vulnerability(self):
        user = UserFactory()
        self.client.force_login(user)
        project = Project.objects.create(name="Test Project", description="Test description")
        vuln = Vulnerability.objects.create(title="Test Vuln", created_at=timezone.now(), reporter=user,
                                            project=project)
        userB = UserFactory()
        self.client.force_login(userB)
        url = reverse("vulnerability-detail", kwargs={"pk": vuln.id})
        data = {
            "status": "fixed",
            "title": "Zmieniony tytuł",
            "severity": "high",
            "description": "Test description",
            "project": vuln.project.id
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code,403)

    def test_create_vulnerability(self):
        user = UserFactory()
        self.client.force_login(user)
        project = Project.objects.create(name="Test Project", description="Test description")
        data = {
            "title": "Test Vuln",
            "description": "Test description",
            "severity": "high",
            "project": project.id
        }
        url = reverse("vulnerability-list")
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code,201)

    def test_delete_vulnerability(self):
        user = UserFactory()
        self.client.force_login(user)
        project = Project.objects.create(name="Test Project", description="Test description")
        vulnerability = Vulnerability.objects.create(title="Test Vuln", reporter=user, project=project)
        data = {
            "title": "Test Vuln",
            "description": "Test description",
            "severity": "high",
            "project": project.id
        }
        url = reverse("vulnerability-detail", kwargs={"pk": vulnerability.id})
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code,204)

    def test_reporter_can_edit(self):
        user = UserFactory()
        self.client.force_login(user)
        project = Project.objects.create(name="Test Project", description="Test description")
        vulnerability = Vulnerability.objects.create(title="Test Vuln", reporter=user, project=project)
        data = {
            "title": "Test New_Vuln",
            "description": "Test description",
            "severity": "high",
            "project":project.id
        }
        url = reverse("vulnerability-detail", kwargs={"pk": vulnerability.id})
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code,200)
class TestProject(APITestCase):

    def test_create_project(self):
        user = UserFactory()
        user.is_staff = True
        self.client.force_login(user)
        data = {"name": "New Project", "description": "New description"}
        url = reverse("project-list")
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code,201)

    def test_update_project(self):
        user = UserFactory()
        self.client.force_login(user)
        project = Project.objects.create(name="Test Project", description="Test description")
        data = {"name": "New Project", "description": "New description"}
        url = reverse("project-detail", kwargs={"pk": project.id})
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code,200)

    def test_delete_project(self):
        user = UserFactory()
        self.client.force_login(user)
        project = Project.objects.create(name="Test Project", description="Test description")
        url = reverse("project-detail", kwargs={"pk": project.id})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code,204)

class TestFilter(APITestCase):

    def test_ordering_vulnerability(self):
        user = UserFactory()
        self.client.force_login(user)
        project = Project.objects.create(name="Test Project", description="Test description")

        vuln1 = Vulnerability.objects.create(title="Vuln 1", reporter=user, project=project,
                                             created_at=timezone.now() - timezone.timedelta(days=2))
        vuln2 = Vulnerability.objects.create(title="Vuln 2", reporter=user, project=project,
                                             created_at=timezone.now() - timezone.timedelta(days=1))
        vuln3 = Vulnerability.objects.create(title="Vuln 3", reporter=user, project=project, created_at=timezone.now())

        response = self.client.get(reverse('vulnerability-list'), {"ordering": "-created_at"})

        # Sprawdź czy vuln3 (newest) jest pierwszy
        self.assertEqual(response.data['results'][0]['title'], "Vuln 3")
        self.assertEqual(response.data['results'][2]['title'], "Vuln 1")