import logging

from django.test import TestCase

from core.api import login_test
from apps.users.models import USER_ROLE_ID, User


logging.disable(logging.CRITICAL)


class PermissionsTestCase(TestCase):
    fixtures = ['settings.json', 'roles.json', 'admin.json']

    def test_views_permissions_admin(self):
        header = login_test(self.client.post, 'admin', '123')
        urls = [
            '/api/v1/version/',
            '/api/v1/settings/',
            '/api/v1/settings/1'
        ]
        for url in urls:
            response = self.client.get(url, HTTP_AUTHORIZATION=header)
            self.assertEqual(response.status_code, 200)

    def test_views_permissions_user(self):
        # Create user for test
        bob = User.objects.create(
            id=100,
            username='bob',
            email='bob@example.com',
            role_id=USER_ROLE_ID,
            is_active=True
        )
        bob.set_password('bobs-password')
        bob.save()

        header = login_test(self.client.post, 'bob', 'bobs-password')
        urls = [
            '/api/v1/version/',
            '/api/v1/settings/',
            '/api/v1/settings/1'
        ]
        for url in urls:
            response = self.client.get(url, HTTP_AUTHORIZATION=header)
            self.assertEqual(response.status_code, 403)

    def test_views_permissions_anon(self):
        urls = [
            '/api/v1/version/',
            '/api/v1/settings/',
            '/api/v1/settings/1'
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 401)
