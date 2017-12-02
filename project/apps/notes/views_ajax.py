import json

from django.http import JsonResponse
from django.views.generic import View
from django.db import IntegrityError

from .models import Folder, Notepad, Note, BadInput


class ApiView(View):
    """
    Add list method for dispatcher when id is not
    provided for the GET-method
    """

    # Model's fields that cannot be changed by the clients
    readonly_fields = []

    def clear_input(self, data):
        """Remove readonly fields from client's input"""
        for field in self.readonly_fields:
            if field in data:
                del data[field]

    def dispatch(self, request, *args, **kwargs):
        method = request.method.lower()

        if method == 'get' and 'id' not in self.kwargs:
            handler = getattr(self, 'list', self.http_method_not_allowed)
        elif method in self.http_method_names:
            handler = getattr(self, method, self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed

        return handler(request, *args, **kwargs)


class FolderView(ApiView):
    """Full CRUD for Folders"""

    readonly_fields = ['id', 'html', 'created', 'updated']

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode('utf-8'))
        self.clear_input(data)

        folder = Folder(user=request.user, **data)

        try:
            folder.full_save()
        except BadInput as e:
            response = {'error': str(e)}
            return JsonResponse(response, status=400)

        response = folder.to_dict()
        return JsonResponse(response, status=201)

    def get(self, request, *args, **kwargs):
        folder_id = kwargs.get('id')
        try:
            folder = Folder.objects.get(id=folder_id, user=request.user)
        except Folder.DoesNotExist:
            response = {'error': 'Object not found'}
            return JsonResponse(response, status=404)

        response = folder.to_dict()
        return JsonResponse(response, status=200)

    def list(self, request, *args, **kwargs):
        folders = Folder.objects.filter(user=request.user)
        response = {'folders': [f.to_dict() for f in folders]}
        return JsonResponse(response)

    def put(self, request, *args, **kwargs):
        folder_id = kwargs.get('id')
        try:
            folder = Folder.objects.get(id=folder_id, user=request.user)
        except Folder.DoesNotExist:
            response = {'error': 'Object not found'}
            return JsonResponse(response, status=404)

        data = json.loads(request.body.decode('utf-8'))
        self.clear_input(data)

        for (key, value) in data.items():
            setattr(folder, key, value)

        try:
            folder.full_save()
        except BadInput as e:
            response = {'error': str(e)}
            return JsonResponse(response, status=400)

        response = folder.to_dict()
        return JsonResponse(response, status=200)

    def delete(self, request, *args, **kwargs):
        folder_id = kwargs.get('id')
        try:
            folder = Folder.objects.get(id=folder_id, user=request.user)
        except Folder.DoesNotExist:
            response = {'error': 'Object not found'}
            return JsonResponse(response, status=404)

        try:
            folder.delete()
        except IntegrityError:
            response = {'error': 'Failed to delete the object'}
            return JsonResponse(response, status=400)

        return JsonResponse({}, status=204)


class NotepadView(ApiView):
    """Full CRUD for Notepads"""

    readonly_fields = ['id', 'created', 'updated']

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode('utf-8'))
        self.clear_input(data)

        error = None
        if not data.get('folder_id'):
            error = 'Can\'t make notepad outside folders'
        elif not data.get('title'):
            error = 'Notepad must have title'
        if error:
            return JsonResponse({'error': error}, status=400)

        notepad = Notepad(user=request.user, **data)

        try:
            notepad.full_save()
        except BadInput as e:
            response = {'error': str(e)}
            return JsonResponse(response, status=400)

        response = notepad.to_dict()
        return JsonResponse(response, status=201)

    def get(self, request, *args, **kwargs):
        notepad_id = kwargs.get('id')
        try:
            notepad = Notepad.objects.get(id=notepad_id, user=request.user)
        except Notepad.DoesNotExist:
            response = {'error': 'Object not found'}
            return JsonResponse(response, status=404)

        response = notepad.to_dict()
        return JsonResponse(response, status=200)

    def list(self, request, *args, **kwargs):
        folder_id = request.GET.get('folder-id')

        notepads = Notepad.objects.filter(user=request.user)
        if folder_id:
            notepads = notepads.filter(folder_id=folder_id)

        response = {'notepads': [n.to_dict() for n in notepads]}
        return JsonResponse(response)

    def put(self, request, *args, **kwargs):
        notepad_id = kwargs.get('id')
        try:
            notepad = Notepad.objects.get(id=notepad_id, user=request.user)
        except Notepad.DoesNotExist:
            response = {'error': 'Object not found'}
            return JsonResponse(response, status=404)

        data = json.loads(request.body.decode('utf-8'))
        self.clear_input(data)

        for (key, value) in data.items():
            setattr(notepad, key, value)

        try:
            notepad.full_save()
        except BadInput as e:
            response = {'error': str(e)}
            return JsonResponse(response, status=400)

        response = notepad.to_dict()
        return JsonResponse(response, status=200)

    def delete(self, request, *args, **kwargs):
        notepad_id = kwargs.get('id')
        try:
            notepad = Notepad.objects.get(id=notepad_id, user=request.user)
        except Notepad.DoesNotExist:
            response = {'error': 'Object not found'}
            return JsonResponse(response, status=404)

        try:
            notepad.delete()
        except IntegrityError:
            response = {'error': 'Failed to delete the object'}
            return JsonResponse(response, status=400)

        return JsonResponse({}, status=204)


class NoteView(ApiView):
    """Full CRUD for Notes"""

    readonly_fields = ['id', 'html', 'created', 'updated']

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode('utf-8'))
        self.clear_input(data)

        error = None
        if not data.get('notepad_id'):
            error = 'Can\'t make note outside notepads'
        elif not data.get('title'):
            error = 'Note must have title'
        if error:
            return JsonResponse({'error': error}, status=400)

        note = Note(user=request.user, **data)

        try:
            note.full_save()
        except BadInput as e:
            response = {'error': str(e)}
            return JsonResponse(response, status=400)

        response = {'id': note.id}
        return JsonResponse(response, status=201)

    def get(self, request, *args, **kwargs):
        note_id = kwargs.get('id')
        try:
            note = Note.objects.get(id=note_id, user=request.user)
        except Note.DoesNotExist:
            response = {'error': 'Object not found'}
            return JsonResponse(response, status=404)
        response = note.to_dict()
        return JsonResponse(response, status=200)

    def list(self, request, *args, **kwargs):
        notepad_id = request.GET.get('notepad-id')

        notes = Note.objects.filter(user=request.user)
        if notepad_id:
            notes = notes.filter(notepad_id=notepad_id)

        response = {'notes': [n.to_dict() for n in notes]}
        return JsonResponse(response)

    def put(self, request, *args, **kwargs):
        note_id = kwargs.get('id')
        try:
            note = Note.objects.get(id=note_id, user=request.user)
        except Note.DoesNotExist:
            response = {'error': 'Object not found'}
            return JsonResponse(response, status=404)

        data = json.loads(request.body.decode('utf-8'))
        self.clear_input(data)

        for (key, value) in data.items():
            setattr(note, key, value)

        try:
            note.full_save()
        except BadInput as e:
            response = {'error': str(e)}
            return JsonResponse(response, status=400)

        response = note.to_dict()
        return JsonResponse(response, status=200)

    def delete(self, request, *args, **kwargs):
        note_id = kwargs.get('id')
        try:
            note = Note.objects.get(id=note_id, user=request.user)
        except Note.DoesNotExist:
            response = {'error': 'Object not found'}
            return JsonResponse(response, status=404)

        try:
            note.delete()
        except IntegrityError:
            response = {'error': 'Failed to delete the object'}
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
