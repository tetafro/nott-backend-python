import json
from datetime import datetime

from django.contrib import auth
from django.test import TestCase

from apps.users.models import User
from .models import Folder, Notepad, Note


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
        folder1 = Folder.objects.create(
            id=100,
            title='Folder 1',
            user=bob,
            parent=None
        )
        Folder.objects.create(
            id=101,
            title='Folder 2',
            user=bob,
            parent=folder1
        )

    def test_serializer(self):
        try:
            folder = Folder.objects.get(id=101)
        except Folder.DoesNotExist:
            self.fail("Folder not found")

        d = folder.to_dict()
        self.assertEqual(d.get('id'), 101)
        self.assertEqual(d.get('title'), 'Folder 2')
        self.assertEqual(d.get('parent_id'), 100)
        self.assertEqual(type(d.get('created')), datetime)
        self.assertEqual(type(d.get('updated')), datetime)

    def test_create(self):
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
        resp_content = json.loads(response.content.decode('utf-8'))
        self.assertTrue('id' in resp_content)
        self.assertTrue(resp_content is not None)
        id = resp_content['id']

        # Get from server and check
        response = self.client.get('/ajax/folders/%d' % id)
        self.assertEqual(response.status_code, 200)
        folder = json.loads(response.content.decode('utf-8'))
        self.assertEqual(folder.get('id'), id)
        self.assertEqual(folder.get('title'), 'My Folder')
        self.assertEqual(folder.get('parent_id'), None)

    def test_list(self):
        self.client.login(username='bob', password='bobs-password')
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated())

        response = self.client.get('/ajax/folders')
        self.assertEqual(response.status_code, 200)
        resp_content = json.loads(response.content.decode('utf-8'))
        self.assertTrue('folders' in resp_content)
        folders = resp_content['folders']
        self.assertEqual(len(folders), 2)

        # Folder 1
        self.assertEqual(folders[0].get('id'), 100)
        self.assertEqual(folders[0].get('title'), 'Folder 1')
        self.assertEqual(folders[0].get('parent_id'), None)
        # Folder 2
        self.assertEqual(folders[1].get('id'), 101)
        self.assertEqual(folders[1].get('title'), 'Folder 2')
        self.assertEqual(folders[1].get('parent_id'), 100)

    def test_get(self):
        pass


class NotepadsTestCase(TestCase):
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
        folder = Folder.objects.create(
            id=100,
            title='Folder',
            user=bob,
            parent=None
        )
        notepad = Notepad.objects.create(
            id=200,
            title='Notepad',
            user=bob,
            folder=folder
        )

    def test_serializer(self):
        try:
            notepad = Notepad.objects.get(id=200)
        except Notepad.DoesNotExist:
            self.fail("Notepad not found")

        n = notepad.to_dict()
        self.assertEqual(n.get('id'), 200)
        self.assertEqual(n.get('title'), 'Notepad')
        self.assertEqual(n.get('folder_id'), 100)
        self.assertEqual(type(n.get('created')), datetime)
        self.assertEqual(type(n.get('updated')), datetime)


class NotesTestCase(TestCase):
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
        folder = Folder.objects.create(
            id=100,
            title='Folder',
            user=bob,
            parent=None
        )
        notepad = Notepad.objects.create(
            id=200,
            title='Notepad',
            user=bob,
            folder=folder
        )
        note = Note.objects.create(
            id=300,
            title='Note',
            text='Hello, world!',
            user=bob,
            notepad=notepad
        )

    def test_serializer(self):
        try:
            note = Note.objects.get(id=300)
        except Note.DoesNotExist:
            self.fail("Note not found")

        n = note.to_dict()
        self.assertEqual(n.get('id'), 300)
        self.assertEqual(n.get('title'), 'Note')
        self.assertEqual(n.get('text'), 'Hello, world!')
        self.assertEqual(n.get('notepad_id'), 200)
        self.assertEqual(type(n.get('created')), datetime)
        self.assertEqual(type(n.get('updated')), datetime)
