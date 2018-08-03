import json

from django.db import IntegrityError
from django.views.generic import View

from core.api import ApiView, JsonResponse, JsonErrorResponse, \
    JsonResponse404, JsonResponse500
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
            return JsonErrorResponse(str(e), status=400)

        response = folder.to_dict()
        return JsonResponse(response, status=201)

    def get(self, request, *args, **kwargs):
        folder_id = kwargs.get('id')
        try:
            folder = Folder.objects.get(id=folder_id, user=request.user)
        except Folder.DoesNotExist:
            response = {'error': 'object not found'}
            return JsonErrorResponse(response, status=404)

        response = folder.to_dict()
        return JsonResponse(response, status=200)

    def list(self, request, *args, **kwargs):
        folders = Folder.objects.filter(user=request.user)
        response = [f.to_dict() for f in folders]
        return JsonResponse(response)

    def put(self, request, *args, **kwargs):
        folder_id = kwargs.get('id')
        try:
            folder = Folder.objects.get(id=folder_id, user=request.user)
        except Folder.DoesNotExist:
            return JsonResponse404

        data = json.loads(request.body.decode('utf-8'))

        for (key, value) in data.items():
            if key in self.editable_fields:
                setattr(folder, key, value)

        try:
            folder.full_save()
        except BadInput as e:
            return JsonErrorResponse(str(e), status=400)

        response = folder.to_dict()
        return JsonResponse(response, status=200)

    def delete(self, request, *args, **kwargs):
        folder_id = kwargs.get('id')
        try:
            folder = Folder.objects.get(id=folder_id, user=request.user)
        except Folder.DoesNotExist:
            return JsonResponse404

        try:
            folder.delete()
        except IntegrityError:
            return JsonErrorResponse('failed to delete the object', status=400)

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
            error = 'can\'t make notepad outside folders'
        elif not data.get('title'):
            error = 'notepad must have title'
        if error:
            return JsonErrorResponse(error, status=400)

        notepad = Notepad(user=request.user, **data)

        try:
            notepad.full_save()
        except BadInput as e:
            return JsonErrorResponse(str(e), status=400)

        response = notepad.to_dict()
        return JsonResponse(response, status=201)

    def get(self, request, *args, **kwargs):
        notepad_id = kwargs.get('id')
        try:
            notepad = Notepad.objects.get(id=notepad_id, user=request.user)
        except Notepad.DoesNotExist:
            return JsonResponse404

        response = notepad.to_dict()
        return JsonResponse(response, status=200)

    def list(self, request, *args, **kwargs):
        folder_id = request.GET.get('folder-id')

        notepads = Notepad.objects.filter(user=request.user)
        if folder_id:
            notepads = notepads.filter(folder_id=folder_id)

        response = [n.to_dict() for n in notepads]
        return JsonResponse(response)

    def put(self, request, *args, **kwargs):
        notepad_id = kwargs.get('id')
        try:
            notepad = Notepad.objects.get(id=notepad_id, user=request.user)
        except Notepad.DoesNotExist:
            return JsonResponse404

        data = json.loads(request.body.decode('utf-8'))

        for (key, value) in data.items():
            if key in self.editable_fields:
                setattr(notepad, key, value)

        try:
            notepad.full_save()
        except BadInput as e:
            return JsonErrorResponse(str(e), status=400)

        response = notepad.to_dict()
        return JsonResponse(response, status=200)

    def delete(self, request, *args, **kwargs):
        notepad_id = kwargs.get('id')
        try:
            notepad = Notepad.objects.get(id=notepad_id, user=request.user)
        except Notepad.DoesNotExist:
            return JsonResponse404

        try:
            notepad.delete()
        except IntegrityError:
            return JsonErrorResponse('failed to delete the object', status=400)

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
            error = 'can\'t make note outside notepads'
        elif not data.get('title'):
            error = 'note must have title'
        if error:
            return JsonErrorResponse(error, status=400)

        note = Note(user=request.user, **data)

        try:
            note.full_save()
        except BadInput as e:
            return JsonErrorResponse(str(e), status=400)

        response = {'id': note.id}
        return JsonResponse(response, status=201)

    def get(self, request, *args, **kwargs):
        note_id = kwargs.get('id')
        try:
            note = Note.objects.get(id=note_id, user=request.user)
        except Note.DoesNotExist:
            return JsonResponse404
        response = note.to_dict()
        return JsonResponse(response, status=200)

    def list(self, request, *args, **kwargs):
        notepad_id = request.GET.get('notepad-id')

        notes = Note.objects.filter(user=request.user)
        if notepad_id:
            notes = notes.filter(notepad_id=notepad_id)

        response = [n.to_dict() for n in notes]
        return JsonResponse(response)

    def put(self, request, *args, **kwargs):
        note_id = kwargs.get('id')
        try:
            note = Note.objects.get(id=note_id, user=request.user)
        except Note.DoesNotExist:
            return JsonResponse404

        data = json.loads(request.body.decode('utf-8'))

        for (key, value) in data.items():
            if key in self.editable_fields:
                setattr(note, key, value)

        try:
            note.full_save()
        except BadInput as e:
            return JsonErrorResponse(str(e), status=400)

        response = note.to_dict()
        return JsonResponse(response, status=200)

    def delete(self, request, *args, **kwargs):
        note_id = kwargs.get('id')
        try:
            note = Note.objects.get(id=note_id, user=request.user)
        except Note.DoesNotExist:
            return JsonResponse404

        try:
            note.delete()
        except IntegrityError:
            return JsonErrorResponse('failed to delete the object', status=400)

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
            response = {'error': 'no key provided'}
            status = 400

        return JsonResponse(response, status=status)
