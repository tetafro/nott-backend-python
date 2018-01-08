import json
import logging

from django.test import TestCase

from core.api import login_test
from .models import USER_ROLE_ID, User, Token


logging.disable(logging.CRITICAL)


class PermissionsTestCase(TestCase):
    fixtures = ['roles.json', 'admin.json']

    def test_views_permissions_admin(self):
        header = login_test(self.client.post, 'admin', '123')
        urls = [
            '/api/v1/users',
            '/api/v1/users/1',
            '/api/v1/users/me'
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
            '/api/v1/users',
            '/api/v1/users/1'
        ]
        for url in urls:
            response = self.client.get(url, HTTP_AUTHORIZATION=header)
            self.assertEqual(response.status_code, 403)

        response = self.client.get('/api/v1/users/me', HTTP_AUTHORIZATION=header)
        self.assertEqual(response.status_code, 200)

    def test_views_permissions_anon(self):
        urls = [
            '/api/v1/users',
            '/api/v1/users/1',
            '/api/v1/users/me'
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 401)


class UserTestCase(TestCase):
    fixtures = ['roles.json', 'admin.json']

    def test_fixtures(self):
        admin = User.objects.get(username='admin')
        self.assertEqual(admin.is_admin, True)
        self.assertEqual(admin.get_full_name(), 'admin')
        self.assertEqual(admin.get_short_name(), 'admin')

    def test_profile(self):
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

        # Check user in database
        bob = User.objects.get(username='bob')
        self.assertEqual(bob.is_admin, False)
        self.assertEqual(bob.get_full_name(), 'bob')
        self.assertEqual(bob.get_short_name(), 'bob')

        # Get profile using API
        header = login_test(self.client.post, 'bob', 'bobs-password')
        response = self.client.get('/api/v1/users/me', HTTP_AUTHORIZATION=header)
        self.assertEqual(response.status_code, 200)

        profile = json.loads(response.content.decode('utf-8'))
        self.assertEqual(profile.get('username'), 'bob')
        self.assertEqual(profile.get('email'), 'bob@example.com')
        self.assertEqual(profile.get('role'), {'name': 'user'})


class AuthTestCase(TestCase):
    fixtures = ['roles.json']

    def test_register(self):
        # Success
        form = {
            'username': 'bob',
            'email': 'bob@example.com',
            'password1': 'bobs-password',
            'password2': 'bobs-password'
        }
        response = self.client.post(
            '/api/v1/register',
            content_type='application/json',
            data=json.dumps(form)
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode('utf-8'))
        self.assertIn('token', data)

        # Validation fails
        forms = [
            # Wrong password confirmation
            {
                'username': 'bob',
                'email': 'bob@example.com',
                'password1': 'bobs-password',
                'password2': 'not-bobs-password'
            },
            # No username
            {
                'email': 'bob@example.com',
                'password1': 'bobs-password',
                'password2': 'bobs-password'
            },
            # No email
            {
                'username': 'bob',
                'password1': 'bobs-password',
                'password2': 'bobs-password'
            },
            # No password
            {
                'username': 'bob',
                'email': 'bob@example.com',
                'password2': 'bobs-password',
            },
            # No password confirmation
            {
                'username': 'bob',
                'email': 'bob@example.com',
                'password1': 'bobs-password',
            },
            # Empty username
            {
                'username': 'bob',
                'email': 'bob@example.com',
                'password1': 'bobs-password',
                'password2': 'not-bobs-password'
            },
            # Empty email
            {
                'username': 'bob',
                'email': 'bob@example.com',
                'password1': 'bobs-password',
                'password2': 'not-bobs-password'
            },
            # Empty password
            {
                'username': 'bob',
                'email': 'bob@example.com',
                'password1': 'bobs-password',
                'password2': 'not-bobs-password'
            },
            # Empty password confirmation
            {
                'username': 'bob',
                'email': 'bob@example.com',
                'password1': 'bobs-password',
                'password2': 'not-bobs-password'
            },
        ]
        for form in forms:
            response = self.client.post(
                '/api/v1/register',
                content_type='application/json',
                data=json.dumps(form)
            )
            self.assertEqual(response.status_code, 400)

    def test_login(self):
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

        # Success
        creds = {
            'username': 'bob',
            'password': 'bobs-password'
        }
        response = self.client.post(
            '/api/v1/login',
            content_type='application/json',
            data=json.dumps(creds)
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode('utf-8'))
        self.assertIn('token', data)

        # Fail
        creds = {
            'username': 'bob',
            'password': 'wrong-password'
        }
        response = self.client.post(
            '/api/v1/login',
            content_type='application/json',
            data=json.dumps(creds)
        )
        self.assertEqual(response.status_code, 400)

    def test_logout(self):
        # Create user with auth token
        bob = User.objects.create(
            id=100,
            username='bob',
            email='bob@example.com',
            role_id=USER_ROLE_ID,
            is_active=True
        )
        token = Token.objects.create(string='123', user=bob)
        token.save()

        # Success
        response = self.client.post(
            '/api/v1/logout',
            HTTP_AUTHORIZATION='Token token="123"'
        )
        self.assertEqual(response.status_code, 200)

        # Fail - invalid token
        response = self.client.post(
            '/api/v1/logout',
            HTTP_AUTHORIZATION='Token token="456"'
        )
        self.assertEqual(response.status_code, 401)

        # Fail - no auth header
        response = self.client.post('/api/v1/logout')
        self.assertEqual(response.status_code, 401)
