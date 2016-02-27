# Standard modules
import json

# Django modules
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

# Auth
from django.contrib.auth.decorators import login_required

# Helpers
from django.http import QueryDict

# Models
from django.contrib.auth.models import User
from apps.data.models import Folder, Notepad, Note

# Custom helpers
from .helpers import object_required, object_save, ajax_response


class FolderView(View):
    """Full CRUD for Folders"""

    def post(self, request, *args, **kwargs):
        data = QueryDict(request.body).dict()
        folder = Folder(user=request.user, **data)

        save_result = object_save(folder)
        if save_result is True:
            response = {'id': folder.id}
            return ajax_response(response, 201)
        else:
            return ajax_response(*save_result)

    @object_required(Folder)
    def get(self, request, *args, **kwargs):
        folder_id = self.kwargs['folder_id']
        folder = Folder.objects.get(id=folder_id)
        notepads = list(folder.notepads.all().order_by('title').values('id', 'title'))

        response = {'notes': notepads}
        return ajax_response(response, 200)

    @object_required(Folder)
    def put(self, request, *args, **kwargs):
        folder_id = self.kwargs['folder_id']
        folder = Folder.objects.get(id=folder_id)
        data = QueryDict(request.body).dict()

        for (key, value) in data.items():
            setattr(folder, key, value)

        save_result = object_save(folder)
        if save_result is True:
            return ajax_response('', 204)
        else:
            return ajax_response(*save_result)

    @object_required(Folder)
    def delete(self, request, *args, **kwargs):
        folder_id = self.kwargs['folder_id']
        folder = Folder.objects.get(id=folder_id)

        try:
            folder.delete()
        except IntegrityError as e:
            response = {'error': 'Bad request'}
            return ajax_response(response, 400)

        return ajax_response('', 204)


class NotepadView(View):
    """Full CRUD for Notepads"""

    def post(self, request, *args, **kwargs):
        data = QueryDict(request.body).dict()
        if not data.get('folder_id') or not data.get('title'):
            response = {'error': 'Bad request'}
            return ajax_response(response, 400)

        notepad = Notepad(**data)

        save_result = object_save(notepad)
        if save_result is True:
            response = {'id': notepad.id}
            return ajax_response(response, 201)
        else:
            return ajax_response(*save_result)

    @object_required(Notepad)
    def get(self, request, *args, **kwargs):
        notepad_id = self.kwargs['notepad_id']
        notepad = Notepad.objects.get(id=notepad_id)
        notes = list(notepad.notes.all().order_by('title').values('id', 'title'))

        response = {'notes': notes}
        return ajax_response(response, 200)

    @object_required(Notepad)
    def put(self, request, *args, **kwargs):
        notepad_id = self.kwargs['notepad_id']
        notepad = Notepad.objects.get(id=notepad_id)
        data = QueryDict(request.body).dict()

        for (key, value) in data.items():
            setattr(notepad, key, value)

        save_result = object_save(notepad)
        if save_result is True:
            return ajax_response('', 204)
        else:
            return ajax_response(save_result)

    @object_required(Notepad)
    def delete(self, request, *args, **kwargs):
        notepad_id = self.kwargs['notepad_id']
        notepad = Notepad.objects.get(id=notepad_id)

        try:
            notepad.delete()
        except IntegrityError as e:
            response = {'error': 'Bad request'}
            return ajax_response(response, 400)

        return ajax_response('', 204)


class NoteView(View):
    """Full CRUD for Notes"""

    def post(self, request, *args, **kwargs):
        data = QueryDict(request.body).dict()
        if not data.get('notepad_id') or not data.get('title'):
            response = {'error': 'Bad request'}
            return response, 400

        note = Note(**data)

        save_result = object_save(note)
        if save_result is True:
            response = {'id': note.id}
            return ajax_response(response, 201)
        else:
            return ajax_response(*save_result)

    @object_required(Note)
    def get(self, request, *args, **kwargs):
        note_id = self.kwargs['note_id']
        note = Note.objects.get(id=note_id)

        response = {'text': note.text}
        return ajax_response(response, 200)

    @object_required(Note)
    def put(self, request, *args, **kwargs):
        note_id = self.kwargs['note_id']
        note = Note.objects.get(id=note_id)
        data = QueryDict(request.body).dict()

        for (key, value) in data.items():
            setattr(note, key, value)

        save_result = object_save(note)
        if save_result is True:
            return ajax_response('', 204)
        else:
            return ajax_response(save_result)

    @object_required(Note)
    def delete(self, request, *args, **kwargs):
        note_id = self.kwargs['note_id']
        note = Note.objects.get(id=note_id)

        try:
            note.delete()
        except IntegrityError as e:
            response = {'error': 'Bad request'}
            return ajax_response(response, 400)

        return ajax_response('', 204)


class SearchView(View):
    """ Search notes with given text """

    def get(self, request, *args, **kwargs):
        text = request.GET.get('text')
        if text:
            notes = list(Note.objects.filter(text__contains=text).values('id', 'title'))
            response = {'notes': notes}
            status = 200
        else:
            response = {'error': 'No text provided'}
            status = 400

        return ajax_response(response, status)
