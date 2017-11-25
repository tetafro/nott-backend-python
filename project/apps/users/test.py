from django.contrib import auth
from django.test import TestCase

from .models import User


class UserTestCase(TestCase):
    fixtures = ['roles.json', 'admin.json']

    def setUp(self):
        User.objects.create(
            id=100,
            username='bob',
            email='bob@example.com',
            role_id=2,
            is_active=True
        )

    def test_fixtures(self):
        admin = User.objects.get(username='admin')
        self.assertEqual(admin.is_admin, True)
        self.assertEqual(admin.get_full_name(), 'admin')
        self.assertEqual(admin.get_short_name(), 'admin')

    def test_user_data(self):
        bob = User.objects.get(username='bob')
        self.assertEqual(bob.is_admin, False)
        self.assertEqual(bob.get_full_name(), 'bob')
        self.assertEqual(bob.get_short_name(), 'bob')


class AuthTestCase(TestCase):
    fixtures = ['roles.json']

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

    def test_redirect_to_login_page(self):
        response = self.client.get('/')
        self.assertRedirects(response, '/login?next=/')

    def test_login_success(self):
        login_form = {
            'username': 'bob',
            'password': 'bobs-password'
        }
        response = self.client.post('/login', login_form, follow=True)
        self.assertRedirects(response, '/')
        self.assertEqual(response.status_code, 200)

    def test_login_fail(self):
        login_form = {
            'username': 'bob',
            'password': 'wrong-password'
        }
        response = self.client.post('/login', login_form)
        self.assertEqual(response.status_code, 400)

    def test_logout_authenticated(self):
        self.client.login(username='bob', password='bobs-password')
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated())
        response = self.client.post('/logout')
        self.assertEqual(response.status_code, 302)

    def test_logout_unauthenticated(self):
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated())
        response = self.client.post('/logout')
        self.assertEqual(response.status_code, 302)

    def test_protected_pages_success(self):
        self.client.login(username='bob', password='bobs-password')
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated())
        response = self.client.get('/users/me')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/users/me/edit')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/users/100')
        self.assertEqual(response.status_code, 200)

    def test_protected_pages_fail(self):
        response = self.client.get('/users/me')
        self.assertRedirects(response, '/login?next=/users/me')
        response = self.client.get('/users/me/edit')
        self.assertRedirects(response, '/login?next=/users/me/edit')
        response = self.client.get('/users/100')
        self.assertRedirects(response, '/login?next=/users/100')
