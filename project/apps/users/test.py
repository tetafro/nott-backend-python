import json
import logging

from django.test import TestCase

from core.api import login_test
from .models import User, Token


logging.disable(logging.CRITICAL)


class PermissionsTestCase(TestCase):
    def setUp(self):
        bob = User.objects.create(
            id=100,
            email='bob@example.com',
            is_active=True
        )
        bob.set_password('123')
        bob.save()

    def test_views_permissions_user(self):
        header = login_test(self.client.post, 'bob@example.com', '123')
        response = self.client.get(
            '/api/v1/profile',
            HTTP_AUTHORIZATION=header
        )
        self.assertEqual(response.status_code, 200)

    def test_views_permissions_anon(self):
        response = self.client.get('/api/v1/profile')
        self.assertEqual(response.status_code, 401)


class UserTestCase(TestCase):
    def setUp(self):
        bob = User.objects.create(
            id=100,
            email='bob@example.com',
            is_active=True
        )
        bob.set_password('123')
        bob.save()

    def test_profile(self):
        # Check user in database
        bob = User.objects.get(email='bob@example.com')
        self.assertEqual(bob.get_full_name(), 'bob@example.com')
        self.assertEqual(bob.get_short_name(), 'bob@example.com')

        # Get profile using API
        header = login_test(self.client.post, 'bob@example.com', '123')
        response = self.client.get(
            '/api/v1/profile',
            HTTP_AUTHORIZATION=header
        )
        self.assertEqual(response.status_code, 200)

        profile = json.loads(response.content.decode('utf-8')).get('data')
        self.assertEqual(profile.get('email'), 'bob@example.com')


class AuthTestCase(TestCase):
    def test_register(self):
        # Success
        form = {
            'email': 'bob@example.com',
            'password': '123',
        }
        response = self.client.post(
            '/api/v1/register',
            content_type='application/json',
            data=json.dumps(form)
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode('utf-8')).get('data')
        self.assertIn('string', data)

        # Validation fails
        forms = [
            # No password
            {
                'email': 'bob@example.com'
            },
            # No email
            {
                'password': '123'
            },
            # Empty email
            {
                'email': '',
                'password': '123'
            },
            # Empty password
            {
                'email': 'bob@example.com',
                'password': ''
            }
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
            email='bob@example.com',
            is_active=True
        )
        bob.set_password('123')
        bob.save()

        # Success
        creds = {
            'email': 'bob@example.com',
            'password': '123'
        }
        response = self.client.post(
            '/api/v1/login',
            content_type='application/json',
            data=json.dumps(creds)
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode('utf-8')).get('data')
        self.assertIn('string', data)

        # Fail
        creds = {
            'email': 'bob@example.com',
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
            email='bob@example.com',
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
