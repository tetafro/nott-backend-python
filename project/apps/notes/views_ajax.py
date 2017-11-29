import json

from django.http import JsonResponse
from django.views.generic import View
from django.db import IntegrityError
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS

from .models import Folder, Notepad, Note
from .helpers import object_required, object_save


class ListableView(View):
    """
    Add list method for dispatcher when id is not
    provided for the GET-method
    """

    def dispatch(self, request, *args, **kwargs):
        method = request.method.lower()

        if method == 'get' and 'id' not in self.kwargs:
            handler = getattr(self, 'list', self.http_method_not_allowed)
        elif method in self.http_method_names:
            handler = getattr(self, method, self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed

        return handler(request, *args, **kwargs)


class FolderView(ListableView):
    """Full CRUD for Folders"""

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode('utf-8'))
        folder = Folder(user=request.user, **data)

        try:
            folder.full_clean()
        except ValidationError as e:
            error_message = ', '.join(e.message_dict[NON_FIELD_ERRORS])
            response = {'error': error_message}
            return response, 400

        try:
            folder.save()
        except IntegrityError as e:
            response = {'error': 'Bad request'}
            return response, 400

        response = {'id': folder.id}
        return JsonResponse(response, status=201)

    @object_required(Folder)
    def get(self, request, *args, **kwargs):
        folder_id = kwargs['id']
        folder = Folder.objects.get(id=folder_id)

        response = {'id': folder.id, 'title': folder.title,
                    'created': folder.created, 'updated': folder.updated}
        return JsonResponse(response, status=200)

    def list(self, request, *args, **kwargs):
        folders = Folder.objects.\
            values('id', 'title', 'parent_id', 'created', 'updated')

        response = {'folders': list(folders)}
        return JsonResponse(response)

    @object_required(Folder)
    def put(self, request, *args, **kwargs):
        folder_id = kwargs['id']
        folder = Folder.objects.get(id=folder_id)
        data = json.loads(request.body.decode('utf-8'))

        for (key, value) in data.items():
            setattr(folder, key, value)

        try:
            folder.full_clean()
        except ValidationError as e:
            error_message = ', '.join(e.message_dict[NON_FIELD_ERRORS])
            response = {'error': error_message}
            return response, 400

        try:
            folder.save()
        except IntegrityError as e:
            response = {'error': 'Bad request'}
            return response, 400

        return JsonResponse({}, status=204)

    @object_required(Folder)
    def delete(self, request, *args, **kwargs):
        folder_id = kwargs['id']
        folder = Folder.objects.get(id=folder_id)

        try:
            folder.delete()
        except IntegrityError as e:
            response = {'error': 'Failed to delete due to integrity error'}
            return JsonResponse(response, status=400)

        return JsonResponse({}, status=204)


class NotepadView(ListableView):
    """Full CRUD for Notepads"""

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode('utf-8'))

        error = None
        if not data.get('folder_id'):
            error = 'Can\'t make notepad outside folders'
        elif not data.get('title'):
            error = 'Notepad must have title'
        if error:
            return JsonResponse({'error': error}, status=400)

        notepad = Notepad(user=request.user, **data)

        try:
            notepad.full_clean()
        except ValidationError as e:
            error_message = ', '.join(e.message_dict[NON_FIELD_ERRORS])
            response = {'error': error_message}
            return response, 400

        try:
            notepad.save()
        except IntegrityError as e:
            response = {'error': 'Bad request'}
            return response, 400

        response = {'id': notepad.id}
        return JsonResponse(response, status=201)

    @object_required(Notepad)
    def get(self, request, *args, **kwargs):
        notepad_id = kwargs['id']
        notepad = Notepad.objects.get(id=notepad_id)

        response = {'id': notepad.id, 'title': notepad.title,
                    'created': notepad.created, 'updated': notepad.updated}
        return JsonResponse(response, status=200)

    def list(self, request, *args, **kwargs):
        folder_id = request.GET.get('folder-id')

        notepads = Notepad.objects.\
            values('id', 'title', 'folder_id', 'created', 'updated')

        if folder_id:
            notepads = notepads.filter(folder_id=folder_id)

        response = {'notepads': list(notepads)}
        return JsonResponse(response)

    @object_required(Notepad)
    def put(self, request, *args, **kwargs):
        notepad_id = kwargs['id']
        notepad = Notepad.objects.get(id=notepad_id)
        data = json.loads(request.body.decode('utf-8'))

        for (key, value) in data.items():
            setattr(notepad, key, value)

        try:
            notepad.full_clean()
        except ValidationError as e:
            error_message = ', '.join(e.message_dict[NON_FIELD_ERRORS])
            response = {'error': error_message}
            return response, 400

        try:
            notepad.save()
        except IntegrityError as e:
            response = {'error': 'Bad request'}
            return response, 400

        return JsonResponse({}, status=204)

    @object_required(Notepad)
    def delete(self, request, *args, **kwargs):
        notepad_id = kwargs['id']
        notepad = Notepad.objects.get(id=notepad_id)

        try:
            notepad.delete()
        except IntegrityError as e:
            response = {'error': 'Failed to delete due to integrity error'}
            return JsonResponse(response, status=400)

        return JsonResponse({}, status=204)


class NoteView(ListableView):
    """Full CRUD for Notes"""

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode('utf-8'))

        error = None
        if not data.get('notepad_id'):
            error = 'Can\'t make note outside notepads'
        elif not data.get('title'):
            error = 'Note must have title'
        if error:
            return JsonResponse({'error': error}, status=400)

        note = Note(user=request.user, **data)

        try:
            note.full_clean()
        except ValidationError as e:
            error_message = ', '.join(e.message_dict[NON_FIELD_ERRORS])
            response = {'error': error_message}
            return response, 400

        try:
            note.save()
        except IntegrityError as e:
            response = {'error': 'Bad request'}
            return response, 400

        response = {'id': note.id}
        return JsonResponse(response, status=201)

    @object_required(Note)
    def get(self, request, *args, **kwargs):
        note_id = kwargs['id']
        note = Note.objects.get(id=note_id)

        response = {'text': note.text, 'html': note.html,
                    'created': note.created, 'updated': note.updated}
        return JsonResponse(response, status=200)

    def list(self, request, *args, **kwargs):
        try:
            notepad_id = request.GET['notepad-id']
        except KeyError:
            response = {'error': 'No notepad id provided'}
            return JsonResponse(response, status=400)

        notes = Note.objects. \
            filter(notepad_id=notepad_id). \
            values('id', 'title', 'notepad_id', 'created', 'updated')

        response = {'notes': list(notes)}
        return JsonResponse(response)

    @object_required(Note)
    def put(self, request, *args, **kwargs):
        note_id = kwargs['id']
        note = Note.objects.get(id=note_id)
        data = json.loads(request.body.decode('utf-8'))

        for (key, value) in data.items():
            setattr(note, key, value)

        try:
            note.full_clean()
        except ValidationError as e:
            error_message = ', '.join(e.message_dict[NON_FIELD_ERRORS])
            response = {'error': error_message}
            return response, 400

        try:
            note.save()
        except IntegrityError as e:
            response = {'error': 'Bad request'}
            return response, 400

        return JsonResponse({}, status=204)

    @object_required(Note)
    def delete(self, request, *args, **kwargs):
        note_id = kwargs['id']
        note = Note.objects.get(id=note_id)

        try:
            note.delete()
        except IntegrityError as e:
            response = {'error': 'Failed to delete due to integrity error'}
            return JsonResponse(response, status=400)

        return JsonResponse({}, status=204)


class SearchView(View):
    """Search notes with given text"""

    def get(self, request, *args, **kwargs):
        key = request.GET.get('key')
        if key:
            notes = list(Note.objects.
                              filter(text__contains=key).
                              values('id', 'title'))
            response = {'notes': notes}
            status = 200
        else:
            response = {'error': 'No key provided'}
            status = 400

        return JsonResponse(response, status=status)
