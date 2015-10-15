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
from data.models import Notepad, Note

# Other helpers
import json


# -----------------------------------------------
# HELPERS                                       -
# -----------------------------------------------

@csrf_exempt
def csrf_failure(request, reason=''):
    """
    Custom error for missing CSRF token
    """

    response = {'error': 'CSRF is missing'}
    return HttpResponse(json.dumps(response), status=400)


def object_required(object_type):
    def decorator(fn):
        def wrapped(request, object_id):
            if object_id is None:
                response = {'error': 'Bad request'}
                return response, 400

            if object_type == 'notepad':
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
# NOTEPADS                                      -
# -----------------------------------------------

def notepad_create(request):
    """ Create notepad """
    data = QueryDict(request.body).dict()
    notepad = Notepad(title=data['title'], user=request.user)
    if 'parent' in data.keys():
        notepad.parent_id = data['parent']

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
    """ Rename notepad """
    if notepad_id is None:
        response = {'error': 'Bad request'}
        return response, 400

    try:
        notepad = Notepad.objects.get(id=notepad_id)
    except Notepad.DoesNotExist:
        response = {'error': 'Notepad not found on server'}
        return response, 400

    data = QueryDict(request.body).dict()
    if 'title' in data:
        notepad.title = data['title']

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
    if notepad_id is None:
        response = {'error': 'Bad request'}
        return response, 400

    try:
        notepad = Notepad.objects.get(id=notepad_id)
    except Notepad.DoesNotExist:
        response = {'error': 'Notepad not found on server'}
        return response, 400

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
    if note_id is None:
        response = {'error': 'Bad request'}
        return response, 400

    try:
        note = Note.objects.get(id=note_id)
    except Note.DoesNotExist:
        response = {'error': 'Note not found on server'}
        return response, 400

    response = {'text': note.text}
    return response, 200


@object_required('note')
def note_update(request, note_id):
    """ Rename note or save new text """
    if note_id is None:
        response = {'error': 'Bad request'}
        return response, 400

    try:
        note = Note.objects.get(id=note_id)
    except Note.DoesNotExist:
        response = {'error': 'Note not found on server'}
        return response, 400

    data = QueryDict(request.body).dict()
    if 'title' in data:
        note.title = data['title']
    if 'text' in data:
        note.text = data['text']

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
    if note_id is None:
        response = {'error': 'Bad request'}
        return response, 400

    try:
        note = Note.objects.get(id=note_id)
    except Note.DoesNotExist:
        response = {'error': 'Note not found on server'}
        return response, 400

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
        response, status = note_update(request, note_id)

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
