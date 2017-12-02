import logging

from django.contrib import auth
from django.test import TestCase

from apps.users.models import User


logging.disable(logging.CRITICAL)


class AdminTestCase(TestCase):
    fixtures = ['config.json', 'roles.json', 'admin.json']

    def setUp(self):
        bob = User.objects.create(
            id=100,
            username='bob',
            email='bob@example.com',
            role_id=2,
            is_active=True
        )
        bob.set_password('bobs-password')
        bob.save()

    def test_protected_pages_success(self):
        self.client.login(username='admin', password='123')
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated())
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)

    def test_protected_pages_fail_user(self):
        self.client.login(username='bob', password='bobs-password')
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated())
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 302)

    def test_protected_pages_fail_anon(self):
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 302)
