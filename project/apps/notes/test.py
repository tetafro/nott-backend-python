import json
import logging
from datetime import datetime

from django.test import TestCase

from core.api import login_test
from apps.users.models import User
from .models import Folder, Notepad, Note


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
        urls = [
            '/api/v1/folders',
            '/api/v1/notepads',
            '/api/v1/notes'
        ]
        for url in urls:
            response = self.client.get(url, HTTP_AUTHORIZATION=header)
            self.assertEqual(response.status_code, 200)

    def test_views_permissions_anon(self):
        urls = [
            '/api/v1/folders',
            '/api/v1/notepads',
            '/api/v1/notes'
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 401)


class FoldersCRUDTestCase(TestCase):
    def setUp(self):
        bob = User.objects.create(
            id=100,
            email='bob@example.com',
            is_active=True
        )
        bob.set_password('123')
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
        folder = Folder.objects.get(id=101)

        d = folder.to_dict()
        self.assertEqual(d.get('id'), 101)
        self.assertEqual(d.get('title'), 'Folder 2')
        self.assertEqual(d.get('parent_id'), 100)
        self.assertEqual(type(d.get('created_at')), datetime)
        self.assertEqual(type(d.get('updated_at')), datetime)

    def test_get_success(self):
        header = login_test(self.client.post, 'bob@example.com', '123')
        response = self.client.get(
            '/api/v1/folders/101',
            HTTP_AUTHORIZATION=header
        )
        self.assertEqual(response.status_code, 200)
        folder = json.loads(response.content.decode('utf-8')).get('data')
        self.assertEqual(folder.get('id'), 101)
        self.assertEqual(folder.get('title'), 'Folder 2')
        self.assertEqual(folder.get('parent_id'), 100)

    def test_get_non_existing_id(self):
        header = login_test(self.client.post, 'bob@example.com', '123')
        response = self.client.get(
            '/api/v1/folders/501',
            HTTP_AUTHORIZATION=header
        )
        self.assertEqual(response.status_code, 404)

    def test_get_malformed_id(self):
        response = self.client.get('/api/v1/folders/abc')
        self.assertEqual(response.status_code, 404)

    def test_list(self):
        header = login_test(self.client.post, 'bob@example.com', '123')
        response = self.client.get(
            '/api/v1/folders',
            HTTP_AUTHORIZATION=header
        )
        self.assertEqual(response.status_code, 200)
        folders = json.loads(response.content.decode('utf-8')).get('data')
        self.assertEqual(len(folders), 2)

        # Folder 1
        self.assertEqual(folders[0].get('id'), 100)
        self.assertEqual(folders[0].get('title'), 'Folder 1')
        self.assertEqual(folders[0].get('parent_id'), None)
        # Folder 2
        self.assertEqual(folders[1].get('id'), 101)
        self.assertEqual(folders[1].get('title'), 'Folder 2')
        self.assertEqual(folders[1].get('parent_id'), 100)

    def test_create_success(self):
        header = login_test(self.client.post, 'bob@example.com', '123')

        # Create
        body = {'title': 'My Folder'}
        response = self.client.post(
            '/api/v1/folders', json.dumps(body), 'application/json',
            HTTP_AUTHORIZATION=header
        )
        self.assertEqual(response.status_code, 201)
        folder = json.loads(response.content.decode('utf-8')).get('data')
        self.assertTrue('id' in folder)
        self.assertTrue(folder is not None)
        id = folder['id']

        # Check
        folder = Folder.objects.get(id=id)
        self.assertEqual(folder.title, 'My Folder')
        self.assertEqual(folder.parent_id, None)

    def test_create_with_readonly_fields(self):
        header = login_test(self.client.post, 'bob@example.com', '123')

        body = {
            'id': 999999,  # will be skipped
            'title': 'New Name',
            'created_at': '2010-10-10T10:10:10.000Z',  # will be skipped
            'updated_at': '2010-10-10T10:10:10.000Z'  # will be skipped
        }
        response = self.client.post(
            '/api/v1/folders', json.dumps(body), 'application/json',
            HTTP_AUTHORIZATION=header
        )
        self.assertEqual(response.status_code, 201)
        folder = json.loads(response.content.decode('utf-8')).get('data')
        self.assertNotEqual(folder.get('id'), body['id'])
        self.assertNotEqual(folder.get('created_at'), body['created_at'])
        self.assertNotEqual(folder.get('updated_at'), body['updated_at'])

    def test_create_empty_body(self):
        header = login_test(self.client.post, 'bob@example.com', '123')

        body = {}
        response = self.client.post(
            '/api/v1/folders', json.dumps(body), 'application/json',
            HTTP_AUTHORIZATION=header
        )
        self.assertEqual(response.status_code, 400)

    def test_modify_success(self):
        header = login_test(self.client.post, 'bob@example.com', '123')

        # Modify
        body = {
            'title': 'New Name',
            'parent_id': None
        }
        response = self.client.put(
            '/api/v1/folders/101', json.dumps(body), 'application/json',
            HTTP_AUTHORIZATION=header
        )
        self.assertEqual(response.status_code, 200)

        # Check
        folder = Folder.objects.get(id=101)
        self.assertEqual(folder.title, 'New Name')
        self.assertEqual(folder.parent_id, None)

    def test_modify_empty_body(self):
        header = login_test(self.client.post, 'bob@example.com', '123')

        # Modify
        body = {}
        response = self.client.put(
            '/api/v1/folders/101', json.dumps(body), 'application/json',
            HTTP_AUTHORIZATION=header
        )
        self.assertEqual(response.status_code, 200)  # nothing happened

        # Get from server and check
        folder = Folder.objects.get(id=101)
        self.assertEqual(folder.title, 'Folder 2')
        self.assertEqual(folder.parent_id, 100)

    def test_modify_non_existing_id(self):
        header = login_test(self.client.post, 'bob@example.com', '123')

        body = {'title': 'New Name'}
        response = self.client.put(
            '/api/v1/folders/501', json.dumps(body), 'application/json',
            HTTP_AUTHORIZATION=header
        )
        self.assertEqual(response.status_code, 404)

    def test_modify_malformed_id(self):
        header = login_test(self.client.post, 'bob@example.com', '123')

        body = {'title': 'New Name'}
        response = self.client.put(
            '/api/v1/folders/abc', json.dumps(body), 'application/json',
            HTTP_AUTHORIZATION=header
        )
        self.assertEqual(response.status_code, 404)

    def test_delete(self):
        header = login_test(self.client.post, 'bob@example.com', '123')

        # Delete
        response = self.client.delete(
            '/api/v1/folders/100',
            HTTP_AUTHORIZATION=header
        )
        self.assertEqual(response.status_code, 204)

        # Check
        def test_check():
            Folder.objects.get(id=100)
        self.assertRaises(Folder.DoesNotExist, test_check)


class FoldersValidationTestCase(TestCase):
    def setUp(self):
        bob = User.objects.create(
            id=100,
            email='bob@example.com',
            is_active=True
        )
        bob.set_password('123')
        bob.save()

    def test_empty_title(self):
        header = login_test(self.client.post, 'bob@example.com', '123')

        body = {'title': ''}
        response = self.client.post(
            '/api/v1/folders', json.dumps(body), 'application/json',
            HTTP_AUTHORIZATION=header
        )
        self.assertEqual(response.status_code, 400)

    def test_long_title(self):
        header = login_test(self.client.post, 'bob@example.com', '123')

        body = {'title': 'a' * 81}
        response = self.client.post(
            '/api/v1/folders', json.dumps(body), 'application/json',
            HTTP_AUTHORIZATION=header
        )
        self.assertEqual(response.status_code, 400)

    def test_non_existing_parent(self):
        header = login_test(self.client.post, 'bob@example.com', '123')

        # Create
        body = {
            'title': 'New Folder',
            'parent_id': 600
        }
        response = self.client.post(
            '/api/v1/folders', json.dumps(body), 'application/json',
            HTTP_AUTHORIZATION=header
        )
        self.assertEqual(response.status_code, 400)


class NotepadsTestCase(TestCase):
    def setUp(self):
        bob = User.objects.create(
            id=100,
            email='bob@example.com',
            is_active=True
        )
        bob.set_password('123')
        bob.save()
        folder = Folder.objects.create(
            id=100,
            title='Folder',
            user=bob,
            parent=None
        )
        Notepad.objects.create(
            id=200,
            title='Notepad 1',
            user=bob,
            folder=folder
        )
        Notepad.objects.create(
            id=201,
            title='Notepad 2',
            user=bob,
            folder=folder
        )

    def test_serializer(self):
        notepad = Notepad.objects.get(id=200)

        n = notepad.to_dict()
        self.assertEqual(n.get('id'), 200)
        self.assertEqual(n.get('title'), 'Notepad 1')
        self.assertEqual(n.get('folder_id'), 100)
        self.assertEqual(type(n.get('created_at')), datetime)
        self.assertEqual(type(n.get('updated_at')), datetime)

    def test_get_success(self):
        header = login_test(self.client.post, 'bob@example.com', '123')

        response = self.client.get(
            '/api/v1/notepads/200',
            HTTP_AUTHORIZATION=header
        )
        self.assertEqual(response.status_code, 200)
        notepad = json.loads(response.content.decode('utf-8')).get('data')
        self.assertEqual(notepad.get('id'), 200)
        self.assertEqual(notepad.get('title'), 'Notepad 1')
        self.assertEqual(notepad.get('folder_id'), 100)

    def test_get_non_existing_id(self):
        header = login_test(self.client.post, 'bob@example.com', '123')

        response = self.client.get(
            '/api/v1/notepads/501',
            HTTP_AUTHORIZATION=header
        )
        self.assertEqual(response.status_code, 404)

    def test_get_malformed_id(self):
        header = login_test(self.client.post, 'bob@example.com', '123')

        response = self.client.get(
            '/api/v1/notepads/abc',
            HTTP_AUTHORIZATION=header
        )
        self.assertEqual(response.status_code, 404)

    def test_list(self):
        header = login_test(self.client.post, 'bob@example.com', '123')

        response = self.client.get(
            '/api/v1/notepads',
            HTTP_AUTHORIZATION=header
        )
        self.assertEqual(response.status_code, 200)
        notepads = json.loads(response.content.decode('utf-8')).get('data')
        self.assertEqual(len(notepads), 2)

        # Notepad 1
        self.assertEqual(notepads[0].get('id'), 200)
        self.assertEqual(notepads[0].get('title'), 'Notepad 1')
        self.assertEqual(notepads[0].get('folder_id'), 100)
        # Notepad 2
        self.assertEqual(notepads[1].get('id'), 201)
        self.assertEqual(notepads[1].get('title'), 'Notepad 2')
        self.assertEqual(notepads[1].get('folder_id'), 100)

    def test_create(self):
        header = login_test(self.client.post, 'bob@example.com', '123')

        # Create
        body = {
            'title': 'My Notepad',
            'folder_id': 100
        }
        response = self.client.post(
            '/api/v1/notepads', json.dumps(body), 'application/json',
            HTTP_AUTHORIZATION=header
        )
        self.assertEqual(response.status_code, 201)
        notepad = json.loads(response.content.decode('utf-8')).get('data')
        self.assertTrue(notepad is not None)
        self.assertTrue('id' in notepad)
        id = notepad['id']

        # Check
        notepad = Notepad.objects.get(id=id)
        self.assertEqual(notepad.title, 'My Notepad')
        self.assertEqual(notepad.folder_id, 100)

    def test_modify(self):
        header = login_test(self.client.post, 'bob@example.com', '123')

        # Modify
        body = {
            'title': 'New Name',
        }
        response = self.client.put(
            '/api/v1/notepads/200', json.dumps(body), 'application/json',
            HTTP_AUTHORIZATION=header
        )
        self.assertEqual(response.status_code, 200)

        # Check
        notepad = Notepad.objects.get(id=200)
        self.assertEqual(notepad.title, 'New Name')
        self.assertEqual(notepad.folder_id, 100)

    def test_delete(self):
        header = login_test(self.client.post, 'bob@example.com', '123')

        # Delete
        response = self.client.delete(
            '/api/v1/notepads/200',
            HTTP_AUTHORIZATION=header
        )
        self.assertEqual(response.status_code, 204)

        # Check
        def test_check():
            Notepad.objects.get(id=200)
        self.assertRaises(Notepad.DoesNotExist, test_check)


class NotepadsValidationTestCase(TestCase):
    def setUp(self):
        bob = User.objects.create(
            id=100,
            email='bob@example.com',
            is_active=True
        )
        bob.set_password('123')
        bob.save()
        Folder.objects.create(
            id=100,
            title='Folder',
            user=bob,
            parent=None
        )

    def test_empty_title(self):
        header = login_test(self.client.post, 'bob@example.com', '123')

        body = {
            'title': '',
            'folder_id': 100
        }
        response = self.client.post(
            '/api/v1/notepads', json.dumps(body), 'application/json',
            HTTP_AUTHORIZATION=header
        )
        self.assertEqual(response.status_code, 400)

    def test_long_title(self):
        header = login_test(self.client.post, 'bob@example.com', '123')

        body = {
            'title': 'a' * 81,
            'folder_id': 100
        }
        response = self.client.post(
            '/api/v1/notepads', json.dumps(body), 'application/json',
            HTTP_AUTHORIZATION=header
        )
        self.assertEqual(response.status_code, 400)

    def test_empty_folder(self):
        header = login_test(self.client.post, 'bob@example.com', '123')

        body = {'title': 'New Notepad'}
        response = self.client.post(
            '/api/v1/notepads', json.dumps(body), 'application/json',
            HTTP_AUTHORIZATION=header
        )
        self.assertEqual(response.status_code, 400)

    def test_non_existing_folder(self):
        header = login_test(self.client.post, 'bob@example.com', '123')

        # Create
        body = {
            'title': 'New Notepad',
            'folder_id': 600
        }
        response = self.client.post(
            '/api/v1/notepads', json.dumps(body), 'application/json',
            HTTP_AUTHORIZATION=header
        )
        self.assertEqual(response.status_code, 400)


class NotesTestCase(TestCase):
    def setUp(self):
        bob = User.objects.create(
            id=100,
            email='bob@example.com',
            is_active=True
        )
        bob.set_password('123')
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
        Note.objects.create(
            id=300,
            title='Note 1',
            text='Hello, world!',
            user=bob,
            notepad=notepad
        )
        Note.objects.create(
            id=301,
            title='Note 2',
            text='Goodbye, world!',
            user=bob,
            notepad=notepad
        )

    def test_serializer(self):
        note = Note.objects.get(id=300)

        n = note.to_dict()
        self.assertEqual(n.get('id'), 300)
        self.assertEqual(n.get('title'), 'Note 1')
        self.assertEqual(n.get('text'), 'Hello, world!')
        self.assertEqual(n.get('notepad_id'), 200)
        self.assertEqual(type(n.get('created_at')), datetime)
        self.assertEqual(type(n.get('updated_at')), datetime)

    def test_get_success(self):
        header = login_test(self.client.post, 'bob@example.com', '123')

        response = self.client.get(
            '/api/v1/notes/300',
            HTTP_AUTHORIZATION=header
        )
        self.assertEqual(response.status_code, 200)
        note = json.loads(response.content.decode('utf-8')).get('data')
        self.assertEqual(note.get('id'), 300)
        self.assertEqual(note.get('title'), 'Note 1')
        self.assertEqual(note.get('notepad_id'), 200)

    def test_get_non_existing_id(self):
        header = login_test(self.client.post, 'bob@example.com', '123')

        response = self.client.get(
            '/api/v1/notepads/501',
            HTTP_AUTHORIZATION=header
        )
        self.assertEqual(response.status_code, 404)

    def test_get_malformed_id(self):
        header = login_test(self.client.post, 'bob@example.com', '123')

        response = self.client.get(
            '/api/v1/notepads/abc',
            HTTP_AUTHORIZATION=header
        )
        self.assertEqual(response.status_code, 404)

    def test_list(self):
        header = login_test(self.client.post, 'bob@example.com', '123')

        response = self.client.get(
            '/api/v1/notes',
            HTTP_AUTHORIZATION=header
        )
        self.assertEqual(response.status_code, 200)
        notes = json.loads(response.content.decode('utf-8')).get('data')
        self.assertEqual(len(notes), 2)

        # Note 1
        self.assertEqual(notes[0].get('id'), 300)
        self.assertEqual(notes[0].get('title'), 'Note 1')
        self.assertEqual(notes[0].get('notepad_id'), 200)
        # Note 2
        self.assertEqual(notes[1].get('id'), 301)
        self.assertEqual(notes[1].get('title'), 'Note 2')
        self.assertEqual(notes[1].get('notepad_id'), 200)

    def test_create(self):
        header = login_test(self.client.post, 'bob@example.com', '123')

        # Create
        body = {
            'title': 'My Note',
            'notepad_id': 200,
            'text': 'Hello, world'
        }
        response = self.client.post(
            '/api/v1/notes', json.dumps(body), 'application/json',
            HTTP_AUTHORIZATION=header
        )
        self.assertEqual(response.status_code, 201)
        note = json.loads(response.content.decode('utf-8')).get('data')
        id = note['id']

        # Check
        note = Note.objects.get(id=id)
        self.assertEqual(note.title, 'My Note')
        self.assertEqual(note.notepad_id, 200)
        self.assertEqual(note.text, 'Hello, world')

    def test_modify(self):
        header = login_test(self.client.post, 'bob@example.com', '123')

        # Modify
        body = {
            'title': 'New Name',
        }
        response = self.client.put(
            '/api/v1/notes/300', json.dumps(body), 'application/json',
            HTTP_AUTHORIZATION=header
        )
        self.assertEqual(response.status_code, 200)

        # Check
        note = Note.objects.get(id=300)
        self.assertEqual(note.title, 'New Name')

    def test_delete(self):
        header = login_test(self.client.post, 'bob@example.com', '123')

        # Delete
        response = self.client.delete(
            '/api/v1/notes/300',
            HTTP_AUTHORIZATION=header
        )
        self.assertEqual(response.status_code, 204)

        # Check
        def test_check():
            Note.objects.get(id=300)
        self.assertRaises(Note.DoesNotExist, test_check)


class NotesValidationTestCase(TestCase):
    def setUp(self):
        bob = User.objects.create(
            id=100,
            email='bob@example.com',
            is_active=True
        )
        bob.set_password('123')
        bob.save()
        folder = Folder.objects.create(
            id=100,
            title='Folder',
            user=bob,
            parent=None
        )
        Notepad.objects.create(
            id=200,
            title='Notepad',
            user=bob,
            folder=folder
        )

    def test_empty_title(self):
        header = login_test(self.client.post, 'bob@example.com', '123')

        body = {
            'title': '',
            'notepad_id': 200
        }
        response = self.client.post(
            '/api/v1/notes', json.dumps(body), 'application/json',
            HTTP_AUTHORIZATION=header
        )
        self.assertEqual(response.status_code, 400)

    def test_long_title(self):
        header = login_test(self.client.post, 'bob@example.com', '123')

        body = {
            'title': 'a' * 81,
            'notepad_id': 200
        }
        response = self.client.post(
            '/api/v1/notes', json.dumps(body), 'application/json',
            HTTP_AUTHORIZATION=header
        )
        self.assertEqual(response.status_code, 400)

    def test_empty_notepad(self):
        header = login_test(self.client.post, 'bob@example.com', '123')

        body = {'title': 'New Note'}
        response = self.client.post(
            '/api/v1/notes', json.dumps(body), 'application/json',
            HTTP_AUTHORIZATION=header
        )
        self.assertEqual(response.status_code, 400)

    def test_non_existing_notepad(self):
        header = login_test(self.client.post, 'bob@example.com', '123')

        # Create
        body = {
            'title': 'New Note',
            'notepad_id': 600
        }
        response = self.client.post(
            '/api/v1/notes', json.dumps(body), 'application/json',
            HTTP_AUTHORIZATION=header
        )
        self.assertEqual(response.status_code, 400)
