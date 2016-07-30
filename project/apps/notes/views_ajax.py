import json

from django.http import JsonResponse
from django.views.generic import View
from django.db import IntegrityError

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

        save_result = object_save(folder)
        if save_result is True:
            response = {'id': folder.id}
            return JsonResponse(response, status=201)
        else:
            return JsonResponse(*save_result)

    @object_required(Folder)
    def get(self, request, *args, **kwargs):
        folder_id = kwargs['id']
        folder = Folder.objects.get(id=folder_id)

        response = {'id': folder.id, 'title': folder.title}
        return JsonResponse(response, status=200)

    def list(self, request, *args, **kwargs):
        folders = Folder.objects.\
                         all().\
                         order_by('title').\
                         values('id', 'title', 'parent_id')

        response = {'folders': list(folders)}
        return JsonResponse(response)

    @object_required(Folder)
    def put(self, request, *args, **kwargs):
        folder_id = kwargs['id']
        folder = Folder.objects.get(id=folder_id)
        data = json.loads(request.body.decode('utf-8'))

        for (key, value) in data.items():
            setattr(folder, key, value)

        save_result = object_save(folder)
        if save_result is True:
            return JsonResponse({}, status=204)
        else:
            return JsonResponse(*save_result)

    @object_required(Folder)
    def delete(self, request, *args, **kwargs):
        folder_id = kwargs['id']
        folder = Folder.objects.get(id=folder_id)

        try:
            folder.delete()
        except IntegrityError as e:
            response = {'error': 'Bad request'}
            return JsonResponse(response, status=400)

        return JsonResponse({}, status=204)


class NotepadView(ListableView):
    """Full CRUD for Notepads"""

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode('utf-8'))
        if not data.get('folder_id') or not data.get('title'):
            response = {'error': 'Bad request'}
            return JsonResponse(response, status=400)

        notepad = Notepad(**data)

        save_result = object_save(notepad)
        if save_result is True:
            response = {'id': notepad.id}
            return JsonResponse(response, status=201)
        else:
            return JsonResponse(*save_result)

    @object_required(Notepad)
    def get(self, request, *args, **kwargs):
        notepad_id = kwargs['id']
        notepad = Notepad.objects.get(id=notepad_id)

        response = {'id': notepad.id, 'title': notepad.title}
        return JsonResponse(response, status=200)

    def list(self, request, *args, **kwargs):
        folder_id = request.GET.get('folder-id')

        notepads = Notepad.objects.\
                           order_by('title').\
                           values('id', 'title', 'folder_id')

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

        save_result = object_save(notepad)
        if save_result is True:
            return JsonResponse({}, status=204)
        else:
            return JsonResponse(*save_result)

    @object_required(Notepad)
    def delete(self, request, *args, **kwargs):
        notepad_id = kwargs['id']
        notepad = Notepad.objects.get(id=notepad_id)

        try:
            notepad.delete()
        except IntegrityError as e:
            response = {'error': 'Bad request'}
            return JsonResponse(response, status=400)

        return JsonResponse({}, status=204)


class NoteView(ListableView):
    """Full CRUD for Notes"""

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode('utf-8'))
        if not data.get('notepad_id') or not data.get('title'):
            response = {'error': 'Bad request'}
            return JsonResponse(response, status=400)

        note = Note(**data)

        save_result = object_save(note)
        if save_result is True:
            response = {'id': note.id}
            return JsonResponse(response, status=201)
        else:
            return JsonResponse(*save_result)

    @object_required(Note)
    def get(self, request, *args, **kwargs):
        note_id = kwargs['id']
        note = Note.objects.get(id=note_id)

        response = {'text': note.text}
        return JsonResponse(response, status=200)

    def list(self, request, *args, **kwargs):
        try:
            notepad_id = request.GET['notepad-id']
        except KeyError:
            response = {'error': 'No notepad id provided'}
            return JsonResponse(response, status=400)

        # TODO: Remove after testing timeouts
        # import time
        # time.sleep(5000)

        notes = Note.objects. \
            filter(notepad_id=notepad_id). \
            order_by('title'). \
            values('id', 'title')

        response = {'notes': list(notes)}
        return JsonResponse(response)

    @object_required(Note)
    def put(self, request, *args, **kwargs):
        note_id = kwargs['id']
        note = Note.objects.get(id=note_id)
        data = json.loads(request.body.decode('utf-8'))

        for (key, value) in data.items():
            setattr(note, key, value)

        save_result = object_save(note)
        if save_result is True:
            return JsonResponse({}, status=204)
        else:
            return JsonResponse(save_result)

    @object_required(Note)
    def delete(self, request, *args, **kwargs):
        note_id = kwargs['id']
        note = Note.objects.get(id=note_id)

        try:
            note.delete()
        except IntegrityError as e:
            response = {'error': 'Bad request'}
            return JsonResponse(response, status=400)

        return JsonResponse({}, status=204)


class SearchView(View):
    """ Search notes with given text """

    def get(self, request, *args, **kwargs):
        text = request.GET.get('text')
        if text:
            notes = list(Note.objects.
                              filter(text__contains=text).
                              values('id', 'title'))
            response = {'notes': notes}
            status = 200
        else:
            response = {'error': 'No text provided'}
            status = 400

        return JsonResponse(response, status=status)
