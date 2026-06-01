from django.test import TestCase
from django.urls import reverse

from accounts.models import VulnTrackAccounts
from projects.models import Project
from vulnerabilities.models import Vulnerability, History
from notifications.models import Notification


def make_user(username, role=VulnTrackAccounts.Roles.RESEARCHER):
    return VulnTrackAccounts.objects.create_user(username=username, password='pass', role=role)


def make_project():
    return Project.objects.create(name='Test Project', description='desc')


def make_vuln(reporter, project, status='new', severity='low'):
    return Vulnerability.objects.create(
        title='Test Vuln', description='desc',
        severity=severity, status=status,
        reporter=reporter, project=project,
    )


class VulnerabilityCreateTest(TestCase):
    def setUp(self):
        self.user = make_user('researcher')
        self.project = make_project()
        self.client.login(username='researcher', password='pass')

    def test_create_sets_status_to_new(self):
        self.client.post(reverse('create_vulnerability'), {
            'title': 'New Vuln',
            'description': 'desc',
            'severity': 'low',
            'project': self.project.id,
        })
        vuln = Vulnerability.objects.get(title='New Vuln')
        self.assertEqual(vuln.status, 'new')
        self.assertEqual(vuln.reporter, self.user)

    def test_unauthenticated_redirects_to_login(self):
        self.client.logout()
        response = self.client.get(reverse('create_vulnerability'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/', response['Location'])


class StatusChangeTest(TestCase):
    def setUp(self):
        self.reporter = make_user('reporter')
        self.moderator = make_user('mod', role=VulnTrackAccounts.Roles.MODERATOR)
        self.project = make_project()
        self.vuln = make_vuln(self.reporter, self.project)

    def test_researcher_cannot_change_status(self):
        self.client.login(username='reporter', password='pass')
        self.client.post(
            reverse('vulnerability_detail', args=[self.vuln.id]),
            {'status_submit': '1', 'status': 'fixed'},
        )
        self.vuln.refresh_from_db()
        self.assertEqual(self.vuln.status, 'new')

    def test_moderator_can_change_status(self):
        self.client.login(username='mod', password='pass')
        self.client.post(
            reverse('vulnerability_detail', args=[self.vuln.id]),
            {'status_submit': '1', 'status': 'triaged'},
        )
        self.vuln.refresh_from_db()
        self.assertEqual(self.vuln.status, 'triaged')

    def test_status_change_creates_history(self):
        self.client.login(username='mod', password='pass')
        self.client.post(
            reverse('vulnerability_detail', args=[self.vuln.id]),
            {'status_submit': '1', 'status': 'accepted'},
        )
        self.assertEqual(History.objects.filter(vulnerability=self.vuln).count(), 1)

    def test_status_change_sends_notification_to_reporter(self):
        self.client.login(username='mod', password='pass')
        self.client.post(
            reverse('vulnerability_detail', args=[self.vuln.id]),
            {'status_submit': '1', 'status': 'triaged'},
        )
        self.assertTrue(
            Notification.objects.filter(
                recipient=self.reporter,
                type=Notification.NotificationType.STATUS_CHANGE,
            ).exists()
        )


class DeleteVulnerabilityTest(TestCase):
    def setUp(self):
        self.researcher = make_user('researcher')
        self.moderator = make_user('mod', role=VulnTrackAccounts.Roles.MODERATOR)
        self.project = make_project()
        self.vuln = make_vuln(self.researcher, self.project)

    def test_researcher_cannot_delete(self):
        self.client.login(username='researcher', password='pass')
        response = self.client.post(reverse('delete_vulnerability', args=[self.vuln.id]))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Vulnerability.objects.filter(id=self.vuln.id).exists())

    def test_moderator_can_delete(self):
        self.client.login(username='mod', password='pass')
        self.client.post(reverse('delete_vulnerability', args=[self.vuln.id]))
        self.assertFalse(Vulnerability.objects.filter(id=self.vuln.id).exists())


class IndexStatsTest(TestCase):
    def setUp(self):
        self.user = make_user('user')
        self.project = make_project()
        self.client.login(username='user', password='pass')

    def test_open_count_excludes_fixed_and_closed(self):
        make_vuln(self.user, self.project, status='new')
        make_vuln(self.user, self.project, status='triaged')
        make_vuln(self.user, self.project, status='fixed')
        make_vuln(self.user, self.project, status='closed')
        response = self.client.get(reverse('index'))
        self.assertEqual(response.context['open_vulnerabilities'], 2)
        self.assertEqual(response.context['fixed_vulnerabilities'], 1)
