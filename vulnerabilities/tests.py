from django.test import TestCase
from django.urls import reverse
from notifications.models import Notification
from vulnerabilities.models import Comment
from accounts.factories import UserFactory
from projects.models import Project
from vulnerabilities.models import Vulnerability

class VulnerabilitiesIndexTest(TestCase):
    def test_index_login_user_has_access(self):
        index_url = reverse("index")
        response = self.client.get(index_url)
        self.assertEqual(response.status_code, 302)


class VulnerabilitiesPermissionsTest(TestCase):
    def test_moderator_can_change_status(self):
        moderator = UserFactory(role='moderator')
        project = Project.objects.create(name='Test',description='Test')
        vuln=Vulnerability.objects.create(reporter=moderator, project=project)
        self.client.force_login(moderator)
        self.client.post(reverse("vulnerability_detail",kwargs={"id":vuln.id}),
                                   {'status_submit':'true','status':'fixed'})
        vuln.refresh_from_db()
        self.assertEqual(vuln.status, 'fixed')

    def test_researcher_cannot_change_status(self):
        researcher = UserFactory()
        project = Project.objects.create(name="Test Project", description="Test description")
        vuln = Vulnerability.objects.create(title="Test Bug", reporter=researcher, project=project)
        self.client.force_login(researcher)
        self.client.post(reverse("vulnerability_detail",kwargs={"id":vuln.id}),
                         {'status_submit':'true','status':'fixed'})
        vuln.refresh_from_db()
        self.assertEqual(vuln.status, 'new')

    def test_comment_creates_notification(self):
        reporter = UserFactory()
        project = Project.objects.create(name="title", description="Test")
        vulln = Vulnerability.objects.create(reporter=reporter,title="title", project=project)
        user = UserFactory()
        self.client.force_login(user)
        self.client.post(reverse("vulnerability_detail", kwargs={"id": vulln.id}),
                                    {'comment_submit':'true','content':'Test content'})
        notification = Notification.objects.get(recipient=reporter)
        self.assertTrue(Comment.objects.filter(author=user, vulnerability=vulln).exists())
        self.assertTrue(Notification.objects.filter(recipient=reporter).exists())
        self.assertEqual(notification.type, 'comment')


    def test_reporter_no_notification_own_comment(self):
        reporter = UserFactory()
        project = Project.objects.create(name="title", description="Test")
        vulln = Vulnerability.objects.create(reporter=reporter,title="title", project=project)
        self.client.force_login(reporter)
        self.client.post(reverse("vulnerability_detail", kwargs={"id": vulln.id}),
                                    {'comment_submit': 'true', 'content': 'Test content'})
        self.assertTrue(Comment.objects.filter(author=reporter, vulnerability=vulln).exists())
        self.assertFalse(Notification.objects.filter(recipient=reporter).exists())

    def test_notification_has_correct_url(self):
        reporter = UserFactory()
        project = Project.objects.create(name="title", description="Test")
        vulln = Vulnerability.objects.create(reporter=reporter,title="title", project=project)
        user = UserFactory()
        self.client.force_login(user)
        self.client.post(reverse("vulnerability_detail", kwargs={"id": vulln.id}),
                         {'comment_submit': 'true', 'content': 'Test content'})
        notification = Notification.objects.get(recipient=reporter)
        self.assertEqual(notification.url, f"/vulnerabilities/detail/{vulln.id}/")

class VulnerabilitiesTest(TestCase):

    def test_str(self):
        user = UserFactory()
        project = Project.objects.create(name='Test')
        vulnerability = Vulnerability.objects.create(title="Test bug", reporter=user, project=project)
        self.assertEqual(str(vulnerability), "Test bug")


    def test_default_status(self):
        user = UserFactory()
        project = Project.objects.create(name='Test')
        vulnerability = Vulnerability.objects.create(reporter=user, project=project)
        self.assertEqual(vulnerability.status, Vulnerability.Status.new)

    def test_create_vulnerability_ignores_status_field(self):
        user = UserFactory()
        self.client.force_login(user)
        project = Project.objects.create(name='Test')
        self.client.post(reverse("create_vulnerability"), {
            'title': 'windows',
            'description': 'windows vulnerabilities',
            'severity': 'low',
            'project': project.id,
            'status': 'fixed',
        })
        vulnerability = Vulnerability.objects.get(title='windows')
        self.assertEqual(vulnerability.status, Vulnerability.Status.new)


    def test_urls_are_correct_when_using_reverse(self): # /vulnerabilities/create/
        create_url = reverse("create_vulnerability")
        detail_url = reverse("vulnerability_detail",kwargs={"id":1})
        edit_url = reverse("update_vulnerability", kwargs={"id":1})
        delete_url = reverse("delete_vulnerability", kwargs={"id":1})

        self.assertEqual(create_url, "/vulnerabilities/create/")
        self.assertEqual(detail_url, "/vulnerabilities/detail/1/")
        self.assertEqual(edit_url, "/vulnerabilities/edit/1/")
        self.assertEqual(delete_url, "/vulnerabilities/delete/1/")

class VulnerabilityIndexViewTest(TestCase):

    def test_vulnerability_index(self):
        user = UserFactory()
        self.client.force_login(user)
        project = Project.objects.create(name="Test", description="Test")
        vuln = Vulnerability.objects.create(title="SQL Injection",
          description="Test",
          severity="critical",
          status="open",
          reporter=user,
          project=project
        )
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("vulnerabilities", response.context)
        self.assertIn(vuln, response.context['vulnerabilities'])

    def test_create_vulnerability_get_form(self):
        user = UserFactory()
        self.client.force_login(user)
        response = self.client.get(reverse("create_vulnerability"))
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)

    def test_create_vulnerability_post(self):
        user = UserFactory()
        self.client.force_login(user)
        project = Project.objects.create(name="Test", description="Test")
        response = self.client.post(reverse("create_vulnerability"),{
            'title': 'windows',
            'description': 'windows vulnerabilities',
            'severity': 'low',
            'project': project.id
            })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Vulnerability.objects.filter(title="windows").exists())

    def test_update_vulnerability_get(self):
        user = UserFactory()
        self.client.force_login(user)
        project = Project.objects.create(name="Test", description="Test")
        vulln = Vulnerability.objects.create(
            title="windows",
            reporter=user,
            project=project
        )
        response = self.client.get(reverse('update_vulnerability', kwargs={"id":vulln.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].instance, vulln)

    def test_update_vulnerability_post(self):
        user = UserFactory()
        self.client.force_login(user)
        project = Project.objects.create(name="Test", description="Test")
        vulln = Vulnerability.objects.create(title="windows",
            reporter=user,
            project=project
        )
        response = self.client.post(reverse('update_vulnerability',kwargs={"id":vulln.id}),{
            'title': 'update_windows',
            'description': 'windows vulnerabilities',
            'severity': 'low',
            'project': project.id
        })
        vulln.refresh_from_db()
        self.assertEqual(vulln.title, 'update_windows')
        self.assertEqual(response.status_code, 302)

    def test_delete_vulnerability_get(self):
        user = UserFactory()
        user.is_staff = True
        user.save()
        self.client.force_login(user)
        project = Project.objects.create(name="Test", description="Test")
        vulln = Vulnerability.objects.create(
            title="Test",
            reporter=user,
            project=project
        )
        response = self.client.get(reverse("delete_vulnerability", kwargs={"id":vulln.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['vulnerability'], vulln)

    def test_delete_vulnerability_post(self):
        user = UserFactory()
        user.is_staff = True
        user.save()
        self.client.force_login(user)
        project = Project.objects.create(name="Test", description="Test")
        vulln = Vulnerability.objects.create(
            title="Test",
            reporter=user,
            project=project
        )
        response = self.client.post(reverse("delete_vulnerability",kwargs={"id":vulln.id}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Vulnerability.objects.filter(title="Test").exists())

class TestVulnerabilityIndex(TestCase):

    def test_vulnerability_index(self):
        user = UserFactory()
        self.client.force_login(user)
        project = Project.objects.create(name="Test", description="Test")
        vuln = Vulnerability.objects.create(
            title="Test",
            description="Test",
            status="open",
            reporter=user,
            project=project,
            severity="critical"
        )
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("vulnerabilities", response.context)
        self.assertIn(vuln, response.context['vulnerabilities'])
        self.assertEqual(response.context['total_vulnerabilities'],1)
        self.assertEqual(response.context['critical_vulnerabilities'],1)
        self.assertEqual(response.context['fixed_vulnerabilities'],0)
        self.assertEqual(response.context['open_vulnerabilities'],1)

    def test_no_reporter_user_trying_to_update(self):
        user = UserFactory()
        user2 = UserFactory()
        self.client.force_login(user2)
        project = Project.objects.create(name="Test", description="Test")
        vulln = Vulnerability.objects.create(
            title="Test",
            reporter=user,
            project=project
        )
        response = self.client.post(reverse("update_vulnerability", kwargs={"id": vulln.id}))
        self.assertEqual(response.status_code, 403)

    def test_non_staff_cannot_delete(self):
        user = UserFactory()
        self.client.force_login(user)
        project = Project.objects.create(name="Test", description="Test")
        vulln = Vulnerability.objects.create(
            title="Test",
            reporter=user,
            project=project
        )
        response = self.client.post(reverse("delete_vulnerability", kwargs={"id": vulln.id}))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Vulnerability.objects.filter(title="Test").exists())
