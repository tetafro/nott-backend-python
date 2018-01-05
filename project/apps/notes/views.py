import json

from django.db import IntegrityError
from django.http import JsonResponse
from django.views.generic import View

from core.api import ApiView

from .models import Folder, Notepad, Note, BadInput


class FolderView(ApiView):
    """Full CRUD for Folder model"""

    editable_fields = ['title', 'parent_id']

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode('utf-8'))

        for key in list(data.keys()):
            if key not in self.editable_fields:
                data.pop(key)

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

        for (key, value) in data.items():
            if key in self.editable_fields:
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
    """Full CRUD for Notepad model"""

    editable_fields = ['title', 'folder_id']

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode('utf-8'))

        for key in list(data.keys()):
            if key not in self.editable_fields:
                data.pop(key)

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

        for (key, value) in data.items():
            if key in self.editable_fields:
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
    """Full CRUD for Note model"""

    editable_fields = ['title', 'text', 'notepad_id']

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode('utf-8'))

        for key in list(data.keys()):
            if key not in self.editable_fields:
                data.pop(key)

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

        for (key, value) in data.items():
            if key in self.editable_fields:
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
