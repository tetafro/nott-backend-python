# Main
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Validation exceptions
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.db import IntegrityError

# Auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Django helpers
from django.http import QueryDict

# Models
from django.contrib.auth.models import User
from .models import Notepad, Note
from .forms import NotepadForm, NoteForm

# Other helpers
import json


def user_auth(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('index')
            else:
                # TODO: display error: account blocked
                return redirect('login')
        else:
            # TODO: display error: wrong username or password
            return redirect('login')

    context = {}
    return render(request, 'main/auth.html', context)


@login_required
def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
def index(request):
    root_notepads = list(request.user.notepads.filter(parent_id=1).exclude(id=1).order_by('title'))
    notepads = []

    for i, notepad in enumerate(root_notepads):
        notepads += [notepad]
        if notepad.children:
            notepads += list(notepad.children.order_by('title'))

    context = {'notepads': notepads}
    return render(request, 'main/index.html', context)


@login_required
def userlist(request):
    users = User.objects.all()

    context = {'users': users}
    return render(request, 'main/userlist.html', context)


@login_required
def ajax_notepad(request, notepad_id=None):
    # Create notepad
    if request.method == 'POST':
        data = QueryDict(request.body).dict()
        notepad = Notepad(title=data['title'], user=request.user)
        if 'parent' in data.keys():
            notepad.parent_id = data['parent']

        try:
            notepad.full_clean()
        except ValidationError as e:
            error_message = ', '.join(e.message_dict[NON_FIELD_ERRORS])
            response = {'error': error_message}
            return HttpResponse(json.dumps(response), status=400)

        try:
            notepad.save()
        except IntegrityError as e:
            response = {'error': 'Bad request'}
            return HttpResponse(json.dumps(response), status=400)

        response = {'id': notepad.id}
        return HttpResponse(json.dumps(response), status=201, content_type="application/json")

    if notepad_id is not None:
        try:
            notepad = Notepad.objects.get(id=notepad_id)
        except Notepad.DoesNotExist:
            response = {'error': 'Notepad not found on server'}
            return HttpResponse(json.dumps(response), status=400)

        # Get JSON with all notes of active notepad
        if request.method == 'GET':
            notes = notepad.notes.all().order_by('title')

            notes_dict = {}
            for note in notes:
                notes_dict[note.id] = note.title

            response = {'notes': notes_dict}
            return HttpResponse(json.dumps(response), status=200, content_type="application/json")

        # Rename notepad
        if request.method == 'PUT':
            data = QueryDict(request.body).dict()
            notepad.title = data['title']

            try:
                notepad.full_clean()
            except ValidationError as e:
                error_message = ', '.join(e.message_dict[NON_FIELD_ERRORS])
                response = {'error': error_message}
                return HttpResponse(json.dumps(response), status=400)

            try:
                notepad.save()
            except IntegrityError as e:
                response = {'error': 'Bad request'}
                return HttpResponse(json.dumps(response), status=400)

            return HttpResponse('', status=204)

        # Delete notepad
        if request.method == 'DELETE':
            try:
                notepad.delete()
            except IntegrityError as e:
                response = {'error': 'Bad request'}
                return HttpResponse(json.dumps(response), status=400)

            return HttpResponse('', status=204)

    else:
        response = {'error': 'Bad request'}
        return HttpResponse(json.dumps(response), status=400)


@login_required
def ajax_note(request, note_id=None):
    # Create note
    if request.method == 'POST':
        data = QueryDict(request.body).dict()

        try:
            notepad = Notepad.objects.get(id=data['id'])
        except Notepad.DoesNotExist:
            response = {'error': 'Notepad not found on server'}
            return HttpResponse(json.dumps(response), status=400)

        note = Note(title=data['title'], notepad=notepad)

        try:
            note.full_clean()
        except ValidationError as e:
            error_message = ', '.join(e.message_dict[NON_FIELD_ERRORS])
            response = {'error': error_message}
            return HttpResponse(json.dumps(response), status=400)

        try:
            note.save()
        except IntegrityError as e:
            response = {'error': 'Bad request'}
            return HttpResponse(json.dumps(response), status=400)

        response = {'id': note.id}
        return HttpResponse(json.dumps(response), status=201, content_type="application/json")

    if note_id is not None:
        note = Note.objects.get(id=note_id)

        # Get note's content
        if request.method == 'GET':
            text = note.text

            response = {'text': text}
            return HttpResponse(json.dumps(response), status=200, content_type="application/json")

        # Rename note or save new text
        if request.method == 'PUT':
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
                return HttpResponse(json.dumps(response), status=400)

            try:
                note.save()
            except IntegrityError as e:
                response = {'error': 'Bad request'}
                return HttpResponse(json.dumps(response), status=400)

            return HttpResponse('', status=204)

        # Delete note
        if request.method == 'DELETE':
            try:
                note.delete()
            except IntegrityError as e:
                response = {'error': 'Bad request'}
                return HttpResponse(json.dumps(response), status=400)

            return HttpResponse('', status=204)

    else:
        response = {'error': 'Bad request'}
        return HttpResponse(json.dumps(response), status=400)


@csrf_exempt
def test(request):
    return HttpResponse('Hello, world :)', status=200)
    