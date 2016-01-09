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
        def wrapped(request, object_id):
            if object_id is None:
                response = {'error': 'Bad request'}
                return response, 400

            if object_type == 'folder':
                ObjectClass = Folder
            elif object_type == 'notepad':
                ObjectClass = Notepad
            elif object_type == 'note':
                ObjectClass = Note

            if not ObjectClass.objects.filter(id=object_id).exists():
                response = {
                    'error': object_type.capitalize()+' not found on server'
                }
                return response, 400

            return fn(request, object_id)

        return wrapped

    return decorator


# -----------------------------------------------
# FOLDERS                                       -
# -----------------------------------------------

def folder_create(request):
    """ Create folder """
    data = QueryDict(request.body).dict()
    folder = Folder(title=data['title'], user=request.user)
    if 'parent' in data.keys():
        folder.parent_id = data['parent']

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
    return response, 201


@object_required('folder')
def folder_read(request, folder_id):
    """ Get JSON with all notes of active folder """
    folder = Folder.objects.get(id=folder_id)
    notepads = folder.notepads.all().order_by('title')

    notepads_list = []
    for notepad in notepads_list:
        notepads_list += [{'id': notepad.id, 'title': notepad.title}]

    response = {'notes': notepads_list}
    return response, 200


@object_required('folder')
def folder_update(request, folder_id):
    """ Rename and/or move folder """
    folder = Folder.objects.get(id=folder_id)

    data = QueryDict(request.body).dict()
    if 'title' in data:
        folder.title = data['title']
    if 'parent' in data:
        folder.parent_id = data['parent']

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

    return '', 204


@object_required('folder')
def folder_delete(request, folder_id):
    """ Delete folder """
    folder = Folder.objects.get(id=folder_id)

    try:
        folder.delete()
    except IntegrityError as e:
        response = {'error': 'Bad request'}
        return response, 400

    return '', 204


@login_required
def folder_crud(request, folder_id=None):
    """
    Full CRUD for working with folders
    """

    if request.method == 'POST':
        response, status = folder_create(request)

    elif request.method == 'GET':
        response, status = folder_read(request, folder_id)

    elif request.method == 'PUT':
        response, status = folder_update(request, folder_id)

    elif request.method == 'DELETE':
        response, status = folder_delete(request, folder_id)

    return HttpResponse(
        json.dumps(response, sort_keys=False),
        status=status,
        content_type='application/json'
    )


# -----------------------------------------------
# NOTEPADS                                      -
# -----------------------------------------------

def notepad_create(request):
    """ Create notepad """
    data = QueryDict(request.body).dict()
    if not data.get('folder') or not data.get('title'):
        response = {'error': 'Bad request'}
        return response, 400

    notepad = Notepad(title=data['title'], folder_id=data['folder'])

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
    return response, 201


@object_required('notepad')
def notepad_read(request, notepad_id):
    """ Get JSON with all notes of active notepad """
    notepad = Notepad.objects.get(id=notepad_id)
    notes = notepad.notes.all().order_by('title')

    notes_list = []
    for note in notes:
        notes_list += [{'id': note.id, 'title': note.title}]

    response = {'notes': notes_list}
    return response, 200


@object_required('notepad')
def notepad_update(request, notepad_id):
    """ Rename and/or move notepad """
    notepad = Notepad.objects.get(id=notepad_id)

    data = QueryDict(request.body).dict()
    if 'title' in data:
        notepad.title = data['title']
    if 'folder' in data:
        notepad.folder_id = data['folder']

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

    return '', 204


@object_required('notepad')
def notepad_delete(request, notepad_id):
    """ Delete notepad """
    notepad = Notepad.objects.get(id=notepad_id)

    try:
        notepad.delete()
    except IntegrityError as e:
        response = {'error': 'Bad request'}
        return response, 400

    return '', 204


@login_required
def notepad_crud(request, notepad_id=None):
    """
    Full CRUD for working with notepads
    """

    if request.method == 'POST':
        response, status = notepad_create(request)

    elif request.method == 'GET':
        response, status = notepad_read(request, notepad_id)

    elif request.method == 'PUT':
        response, status = notepad_update(request, notepad_id)

    elif request.method == 'DELETE':
        response, status = notepad_delete(request, notepad_id)

    return HttpResponse(
        json.dumps(response, sort_keys=False),
        status=status,
        content_type='application/json'
    )


# -----------------------------------------------
# NOTES                                         -
# -----------------------------------------------

def note_create(request):
    """ Create note """
    data = QueryDict(request.body).dict()

    if not data.get('id'):
        response = {'error': 'Bad request'}
        return response, 400

    try:
        notepad = Notepad.objects.get(id=data['id'])
    except Notepad.DoesNotExist:
        response = {'error': 'Notepad not found on server'}
        return response, 400

    note = Note(title=data['title'], notepad=notepad)

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
    return response, 201


@object_required('note')
def note_read(request, note_id):
    """ Get note's content """
    note = Note.objects.get(id=note_id)

    response = {'text': note.text}
    return response, 200


@object_required('note')
def note_update(request, note_id):
    """ Rename note, move note to other notepad or save new text """
    note = Note.objects.get(id=note_id)

    data = QueryDict(request.body).dict()
    if 'title' in data:
        note.title = data['title']
    if 'text' in data:
        note.text = data['text']
    if 'notepad' in data:
        note.notepad_id = data['notepad']

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

    return '', 204


@object_required('note')
def note_delete(request, note_id):
    """ Delete note """
    note = Note.objects.get(id=note_id)

    try:
        note.delete()
    except IntegrityError as e:
        response = {'error': 'Bad request'}
        return response, 400

    return '', 204


@login_required
def note_crud(request, note_id=None):
    """
    Full CRUD for working with notes
    """

    if request.method == 'POST':
        response, status = note_create(request)

    elif request.method == 'GET':
        response, status = note_read(request, note_id)

    elif request.method == 'PUT':
        response, status = note_update(request, note_id)

    elif request.method == 'DELETE':
        response, status = note_delete(request, note_id)

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
        notes = Note.objects.filter(text__contains=text)
        notes_list = []
        for note in notes:
            notes_list += [{'id': note.id, 'title': note.title}]

        response = {'notes': notes_list}
        status = 200
    else:
        response = {'error': 'No text provided'}
        status = 400

    return HttpResponse(
        json.dumps(response),
        status=status,
        content_type='application/json'
    )
