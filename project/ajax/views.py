# Main
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Validation exceptions
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.db import IntegrityError

# Auth
from django.contrib.auth.decorators import login_required

# Django helpers
from django.http import QueryDict

# Models
from django.contrib.auth.models import User
from data.models import Folder, Notepad, Note

# Other helpers
import json


# -----------------------------------------------
# HELPERS                                       -
# -----------------------------------------------

def object_required(object_type):
    """
    Decocrator for checking if object with given id exists
    """

    def decorator(fn):
        def wrapped(obj):
            if obj.id is None:
                response = {'error': 'Bad request'}
                return response, 400

            if object_type == 'folder':
                ObjectClass = Folder
            elif object_type == 'notepad':
                ObjectClass = Notepad
            elif object_type == 'note':
                ObjectClass = Note

            if not ObjectClass.objects.filter(id=obj.id).exists():
                response = {
                    'error': object_type.capitalize()+' not found on server'
                }
                return response, 400

            return fn(obj)

        return wrapped

    return decorator


def object_save(obj):
    """ Full clean, save and return errors if occured """
    try:
        obj.full_clean()
    except ValidationError as e:
        error_message = ', '.join(e.message_dict[NON_FIELD_ERRORS])
        response = {'error': error_message}
        return response, 400

    try:
        obj.save()
    except IntegrityError as e:
        response = {'error': 'Bad request'}
        return response, 400

    return True


# -----------------------------------------------
# FOLDERS                                       -
# -----------------------------------------------

class FolderCrud(object):
    """
    Full CRUD for working with folders
    """

    def __init__(self, request, id=None):
        self.request = request
        self.data = QueryDict(request.body).dict()
        self.id = id


    def create(self):
        """ Create folder """
        folder = Folder(user=self.request.user, **self.data)

        save_result = object_save(folder)
        if save_result is True:
            response = {'id': folder.id}
            return response, 201
        else:
            return save_result


    @object_required('folder')
    def read(self):
        """ Get JSON with all notes of the folder """
        folder = Folder.objects.get(id=self.id)
        notepads = list(folder.notepads.all().order_by('title').values('id', 'title'))

        response = {'notes': notepads}
        return response, 200


    @object_required('folder')
    def update(self):
        """ Rename and/or move folder """
        folder = Folder.objects.get(id=self.id)
        for (key, value) in self.data.items():
            setattr(folder, key, value)

        save_result = object_save(folder)
        if save_result is True:
            return '', 204
        else:
            return save_result


    @object_required('folder')
    def delete(self):
        """ Delete folder """
        folder = Folder.objects.get(id=self.id)

        try:
            folder.delete()
        except IntegrityError as e:
            response = {'error': 'Bad request'}
            return response, 400

        return '', 204


@login_required
def folder(request, folder_id=None):
    folder = FolderCrud(request, folder_id)

    if request.method == 'POST':
        response, status = folder.create()
    elif request.method == 'GET':
        response, status = folder.read()
    elif request.method == 'PUT':
        response, status = folder.update()
    elif request.method == 'DELETE':
        response, status = folder.delete()

    return HttpResponse(
        json.dumps(response, sort_keys=False),
        status=status,
        content_type='application/json'
    )


# -----------------------------------------------
# NOTEPADS                                      -
# -----------------------------------------------

class NotepadCrud(object):
    """
    Full CRUD for working with notepads
    """

    def __init__(self, request, id=None):
        self.request = request
        self.data = QueryDict(request.body).dict()
        self.id = id


    def create(self):
        """ Create notepad """
        if not self.data.get('folder_id') or not self.data.get('title'):
            response = {'error': 'Bad request'}
            return response, 400

        notepad = Notepad(**self.data)

        save_result = object_save(notepad)
        if save_result is True:
            response = {'id': notepad.id}
            return response, 201
        else:
            return save_result


    @object_required('notepad')
    def read(self):
        """ Get JSON with all notes of active notepad """
        notepad = Notepad.objects.get(id=self.id)
        notes = list(notepad.notes.all().order_by('title').values('id', 'title'))

        response = {'notes': notes}
        return response, 200


    @object_required('notepad')
    def update(self):
        """ Rename and/or move notepad """
        notepad = Notepad.objects.get(id=self.id)

        for (key, value) in self.data.items():
            setattr(notepad, key, value)

        save_result = object_save(notepad)
        if save_result is True:
            return '', 204
        else:
            return save_result


    @object_required('notepad')
    def delete(self):
        """ Delete notepad """
        notepad = Notepad.objects.get(id=self.id)

        try:
            notepad.delete()
        except IntegrityError as e:
            response = {'error': 'Bad request'}
            return response, 400

        return '', 204


@login_required
def notepad(request, notepad_id=None):
    notepad = NotepadCrud(request, notepad_id)

    if request.method == 'POST':
        response, status = notepad.create()
    elif request.method == 'GET':
        response, status = notepad.read()
    elif request.method == 'PUT':
        response, status = notepad.update()
    elif request.method == 'DELETE':
        response, status = notepad.delete()

    return HttpResponse(
        json.dumps(response, sort_keys=False),
        status=status,
        content_type='application/json'
    )


# -----------------------------------------------
# NOTES                                         -
# -----------------------------------------------

class NoteCrud(object):
    """
    Full CRUD for working with notes
    """

    def __init__(self, request, id=None):
        self.request = request
        self.data = QueryDict(request.body).dict()
        self.id = id


    def create(self):
        """ Create note """
        if (
            not self.data.get('notepad_id') or
            not self.data.get('title') or
            not Notepad.objects.filter(id=self.data['notepad_id']).exists()
            ):
            response = {'error': 'Bad request'}
            return response, 400
        else:
            note = Note(**self.data)

        save_result = object_save(note)
        if save_result is True:
            response = {'id': note.id}
            return response, 201
        else:
            return save_result


    @object_required('note')
    def read(self):
        """ Get note's content """
        note = Note.objects.get(id=self.id)

        response = {'text': note.text}
        return response, 200


    @object_required('note')
    def update(self):
        """ Rename note, move note to other notepad or save new text """
        note = Note.objects.get(id=self.id)

        for (key, value) in self.data.items():
            setattr(note, key, value)

        save_result = object_save(note)
        if save_result is True:
            return '', 204
        else:
            return save_result


    @object_required('note')
    def delete(self):
        """ Delete note """
        note = Note.objects.get(id=self.id)

        try:
            note.delete()
        except IntegrityError as e:
            response = {'error': 'Bad request'}
            return response, 400

        return '', 204


@login_required
def note(request, note_id=None):
    note = NoteCrud(request, note_id)

    if request.method == 'POST':
        response, status = note.create()
    elif request.method == 'GET':
        response, status = note.read()
    elif request.method == 'PUT':
        response, status = note.update()
    elif request.method == 'DELETE':
        response, status = note.delete()

    return HttpResponse(
        json.dumps(response),
        status=status,
        content_type='application/json'
    )


# -----------------------------------------------
# SEARCH                                        -
# -----------------------------------------------

@login_required
def search(request):
    """
    Search notes with given text
    """

    text = request.GET.get('text')
    if text:
        notes = list(Note.objects.filter(text__contains=text).values('id', 'title'))
        response = {'notes': notes}
        status = 200
    else:
        response = {'error': 'No text provided'}
        status = 400

    return HttpResponse(
        json.dumps(response),
        status=status,
        content_type='application/json'
    )
