from django.test import TestCase
from .models import Role, User


class UserTestCase(TestCase):
    fixtures = ['roles.json', 'admin.json']

    def setUp(self):
        User.objects.create(
            username='bob',
            email='bob@example.com',
            role_id=1,
            is_active=True
        )
        User.objects.create(
            username='alice',
            email='alice@example.com',
            role_id=2,
            is_active=True
        )

    def test_fixtures(self):
        admin = User.objects.get(username='admin')
        self.assertEqual(admin.is_admin, True)
        self.assertEqual(admin.get_full_name(), 'admin')
        self.assertEqual(admin.get_full_name(), 'admin')

    def test_users_data(self):
        bob = User.objects.get(username='bob')
        self.assertEqual(bob.is_admin, True)
        self.assertEqual(bob.get_full_name(), 'bob')
        self.assertEqual(bob.get_full_name(), 'bob')

        alice = User.objects.get(username='alice')
        self.assertEqual(alice.is_admin, False)
        self.assertEqual(alice.get_full_name(), 'alice')
        self.assertEqual(alice.get_full_name(), 'alice')


class LoginTestCase(TestCase):
    def test_redirect_to_login_page(self):
        response = self.client.get('/', follow=True)
        self.assertRedirects(response, '/login?next=/')

