from django.test import TestCase
from accounts.factories import UserFactory
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
        user = UserFactory()
        self.client.force_login(user)
        response = self.client.get('/projects/')
        self.assertEqual(response.status_code, 200)

class ProjectPermissionsTest(TestCase):
    def test_staff_can_create_project(self):
        self.user = UserFactory()
        self.user.is_staff = True
        self.user.save()
        self.client.force_login(self.user)
        response = self.client.post('/projects/create/', {'name': 'Test', 'description': 'Test'})
        self.assertEqual(Project.objects.filter(name='Test').exists(), True)

    def test_researcher_cannot_create_project(self):
        self.researcher = UserFactory()
        self.client.force_login(self.researcher)
        response = self.client.post('/projects/create/', {'name': 'Test', 'description': 'Test'})
        self.assertEqual(response.status_code, 403)

    def test_staff_can_edit_project(self):
        self.user = UserFactory()
        self.user.is_staff = True
        self.user.save()
        self.client.force_login(self.user)
        project = Project.objects.create(name='Test',description='Test')
        response = self.client.put(f'/projects/update/{project.id}', {'name': 'Test', 'description': 'Test'})
        self.assertEqual(Project.objects.filter(name='Test').exists(), True)

    def test_staff_can_delete_project(self):
        self.user = UserFactory()
        self.user.is_staff = True
        self.user.save()
        self.client.force_login(self.user)
        project = Project.objects.create(name='Test',description='Test')
        response = self.client.post(f'/projects/{project.id}/delete/', {'name': 'Test', 'description': 'Test'})
        self.assertFalse(Project.objects.filter(name='Test').exists())

class ProjectDetailTest(TestCase):
    def test_project_detail_logged_in(self):
        user = UserFactory()
        self.client.force_login(user)
        project = Project.objects.create(name="Test",description="Test")
        response = self.client.get(f'/projects/{project.id}/')
        self.assertEqual(response.status_code, 200)

    def test_project_detail_not_found(self):
        user = UserFactory()
        self.client.force_login(user)
        response = self.client.get(f'/projects/999/')
        self.assertEqual(response.status_code, 404)

    def test_project_create_get_form(self):
        user = UserFactory()
        user.is_staff = True
        user.save()
        self.client.force_login(user)
        response = self.client.get(f"/projects/create/")
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)

    def test_project_update_get_form(self):
        user = UserFactory()
        user.is_staff = True
        user.save()
        self.client.force_login(user)
        project = Project.objects.create(name="Test",description="Test")
        response = self.client.get(f"/projects/{project.id}/update/")
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertEqual(response.context['form'].instance, project)

    def test_project_update_post_invalid_form(self):
        user = UserFactory()
        user.is_staff = True
        user.save()
        self.client.force_login(user)
        project = Project.objects.create(name="Test",description="Test")
        response = self.client.post(f"/projects/{project.id}/update/",{'description': 'Test'})
        self.assertEqual(response.status_code, 200)
        project.refresh_from_db()
        self.assertEqual(project.name, 'Test')

    def test_researcher_cannot_update_project(self):
        user = UserFactory()
        self.client.force_login(user)
        project = Project.objects.create(name="Test",description="Test")
        response = self.client.post(f"/projects/{project.id}/update/",{'name': 'Test', 'description': 'Test'})
        self.assertEqual(response.status_code, 403)

    def test_researcher_cannot_delete_project(self):
        user = UserFactory()
        self.client.force_login(user)
        project = Project.objects.create(name="Test",description="Test")
        response = self.client.post(f"/projects/{project.id}/delete/",{'name': 'Test'})
        self.assertEqual(response.status_code, 403)

    def test_project_delete_get_confirmation(self):
        user = UserFactory()
        user.is_staff = True
        user.save()
        self.client.force_login(user)
        project = Project.objects.create(name="Test",description="Test")
        response = self.client.get(f"/projects/{project.id}/delete/")
        self.assertEqual(response.status_code,200)
        self.assertIn('project', response.context)
