import json

from django.contrib import auth
from django.test import TestCase

from apps.users.models import User


class PagesTestCase(TestCase):
    fixtures = ['config.json', 'roles.json']

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
        self.client.login(username='bob', password='bobs-password')
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated())
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_protected_pages_fail(self):
        response = self.client.get('/')
        self.assertRedirects(response, '/login?next=/')

class FoldersTestCase(TestCase):
    fixtures = ['config.json', 'roles.json']

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

    def test_create_folder(self):
        self.client.login(username='bob', password='bobs-password')
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated())

        # Create
        body = {
            'title': 'My Folder',
            'parent': None
        }
        response = self.client.post(
            '/ajax/folders', json.dumps(body), 'application/json'
        )
        self.assertEqual(response.status_code, 201)

        # Get from server and check
        response = self.client.get('/ajax/folders')
        self.assertEqual(response.status_code, 200)
        resp_content = json.loads(response.content.decode('utf-8'))
        self.assertTrue('folders' in resp_content)
        folders = resp_content['folders']
        self.assertEqual(len(folders), 1)
        folder = folders[0]
        self.assertEqual(folder.get('title'), 'My Folder')
        self.assertEqual(folder.get('parent_id'), None)
