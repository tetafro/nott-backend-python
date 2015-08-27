# Main
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

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
def index(request):
    context = {}
    return render(request, 'main/index.html', context)


@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def ajax_notepad(request, notepad_id=None):
    if notepad_id is not None:
        notepad = Notepad.objects.get(id=notepad_id)

    # Create notepad
    if request.method == 'POST':
        data = QueryDict(request.body).dict()
        notepad = Notepad(title=data['title'], user=request.user)
        notepad.save()

        response = {'id': notepad.id}
        return HttpResponse(json.dumps(response), status=201, content_type="application/json")

    # Get JSON with all notes of active notepad
    if request.method == 'GET':
        notes = notepad.notes.all()

        notes_dict = {}
        for note in notes:
            notes_dict[note.id] = note.title

        response = {'notes': notes_dict}
        return HttpResponse(json.dumps(response), status=200, content_type="application/json")

    # Rename notepad
    if request.method == 'PUT':
        data = QueryDict(request.body).dict()
        notepad.title = data['title']
        notepad.save()

        return HttpResponse('', status=204)

    # Delete notepad
    if request.method == 'DELETE':
        notepad.delete()

        return HttpResponse('', status=204)


@login_required
def ajax_note(request, note_id=None):
    if note_id is not None:
        note = Note.objects.get(id=note_id)

    # Create note
    if request.method == 'POST':
        data = QueryDict(request.body).dict()
        notepad = Notepad.objects.get(id=data['id'])
        note = Note(title=data['title'], notepad=notepad)
        note.save()

        response = {'id': note.id}
        return HttpResponse(json.dumps(response), status=201, content_type="application/json")
    
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
        elif 'text' in data:
            note.text = data['text']
        note.save()

        return HttpResponse('', status=204)

    # Delete note
    if request.method == 'DELETE':
        note.delete()

        return HttpResponse('', status=204)
