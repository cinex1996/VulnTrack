from ApiVulnTrack.factories import ProjectFactory
from django.utils import timezone
from django.test import tag
from rest_framework.test import APITestCase
from django.urls import reverse
from vulnerabilities.models import Vulnerability
from projects.models import Project
from accounts.factories import UserFactory
from unittest.mock import patch
from rest_framework.pagination import PageNumberPagination

class TestVulnerabilityViewSet(APITestCase): 
    def test_vulnerabilities_list(self):
        user = UserFactory()
        self.client.force_login(user)
        project = ProjectFactory()
        vuln=Vulnerability.objects.create(title="Test Vuln",
                                          reporter=user,
                                          project=project)
        response = self.client.get(reverse("vulnerability-list"))
        self.assertEqual(response.status_code,200)
        self.assertIn('title',response.data['results'][0])    
        
    def test_ordering_vulnerability(self):
        user = UserFactory()
        self.client.force_login(user)
        project = ProjectFactory()

        vuln1 = Vulnerability.objects.create(title="Vuln 1", reporter=user, project=project,
                                             created_at=timezone.now() - timezone.timedelta(days=2))
        vuln2 = Vulnerability.objects.create(title="Vuln 2", reporter=user, project=project,
                                             created_at=timezone.now() - timezone.timedelta(days=1))
        vuln3 = Vulnerability.objects.create(title="Vuln 3", reporter=user, project=project, created_at=timezone.now())

        response = self.client.get(reverse('vulnerability-list'), {"ordering": "-created_at"})

        self.assertEqual(response.data['results'][0]['title'], "Vuln 3")
        self.assertEqual(response.data['results'][2]['title'], "Vuln 1")


    def test_get_vulnerability_created_at(self):
        user = UserFactory()
        self.client.force_login(user)
        project = ProjectFactory()
        vuln=Vulnerability.objects.create(title="Test Vuln",created_at=timezone.now(),reporter=user,project=project)
        vuln_next = Vulnerability.objects.create(title="Test Vuln", created_at=timezone.now(),reporter=user,project=project)
        response = self.client.get(reverse("vulnerability-list"), {"ordering": "-created_at"})
        self.assertEqual(response.status_code,200)

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
        project = ProjectFactory()
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
        project = ProjectFactory()
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
        project = ProjectFactory()
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
        project = ProjectFactory()
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

    @patch.object(PageNumberPagination, 'page_size',5)
    def test_pagination_first_page_returns_five_records(self):
            user = UserFactory()
            self.client.force_login(user)
            for i in range(1, 10):
                proj = ProjectFactory()
                Vulnerability.objects.create(title="vuln", reporter=user, project=proj)
            url = reverse('vulnerability-list')
            response = self.client.get(url, {"page":1})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.data["results"]), 5)

    @patch.object(PageNumberPagination, 'page_size', 4)
    def test_pagination_second_page_returns_four_records(self):
        user = UserFactory()
        self.client.force_login(user)
        for i in range(1, 10):
            proj = ProjectFactory()
            Vulnerability.objects.create(title="vuln", reporter=user, project=proj)
        url = reverse('vulnerability-list')
        response = self.client.get(url, {"page": 2})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 4)

    @patch.object(PageNumberPagination, 'page_size', 4)
    def test_pagination_first_page_returns_four_records_and_count(self):
        user = UserFactory()
        self.client.force_login(user)
        for i in range(1, 10):
            proj = ProjectFactory()
            Vulnerability.objects.create(title="vuln", reporter=user, project=proj)
        url = reverse('vulnerability-list')
        response = self.client.get(url, {"page": 2})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 4)
        self.assertEqual(response.data["count"], 9)

    def test_ordering_vulnerability(self):
        user = UserFactory()
        self.client.force_login(user)
        project = ProjectFactory()

        vuln1 = Vulnerability.objects.create(title="Vuln 1", reporter=user, project=project,
                                             created_at=timezone.now() - timezone.timedelta(days=2))
        vuln2 = Vulnerability.objects.create(title="Vuln 2", reporter=user, project=project,
                                             created_at=timezone.now() - timezone.timedelta(days=1))
        vuln3 = Vulnerability.objects.create(title="Vuln 3", reporter=user, project=project, created_at=timezone.now())

        response = self.client.get(reverse('vulnerability-list'), {"ordering": "-created_at"})

        self.assertEqual(response.data['results'][0]['title'], "Vuln 3")
        self.assertEqual(response.data['results'][2]['title'], "Vuln 1")


class TestProjectViewSet(APITestCase):

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
        project = ProjectFactory()
        data = {"name": "New Project", "description": "New description"}
        url = reverse("project-detail", kwargs={"pk": project.id})
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code,200)

    def test_delete_project(self):
        user = UserFactory()
        self.client.force_login(user)
        project = ProjectFactory()
        url = reverse("project-detail", kwargs={"pk": project.id})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code,204)

    def test_projects_list(self):
        user = UserFactory()
        self.client.force_login(user)
        project = ProjectFactory()
        response = self.client.get(reverse("project-list"))

        self.assertEqual(response.status_code, 200)
        self.assertIn('name', response.data['results'][0])

    def test_project_list_filter_is_active_return_correct_result(self):
        user = UserFactory()
        self.client.force_login(user)
        project = ProjectFactory(name="Test Project", is_active=True)
        project_first = ProjectFactory(name="Test", is_active=True)
        project_second = ProjectFactory(name="Test two", is_active=False)
        response = self.client.get(reverse("project-list"), {"is_active": True})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 2)
        self.assertEqual(response.data["results"][0]["name"], "Test Project")
        self.assertEqual(response.data["results"][1]["name"], "Test")
        self.assertNotIn("Test two", [project["name"] for project in response.data["results"]])


    @tag('x')
    def test_project_list_filter_by_name_correct_result(self):
        user = UserFactory()
        self.client.force_login(user)
        ProjectFactory(name="Test")
        ProjectFactory(name="Test")
        ProjectFactory(name="Advanced Project")
        response = self.client.get(reverse("project-list"), {"name": "Test"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 2)
        self.assertEqual(response.data["results"][0]['name'], "Test")
        self.assertEqual(response.data["results"][1]['name'], "Test")
        self.assertNotIn("Advanced Project", [project["name"] for project in response.data["results"]])

        