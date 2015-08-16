from django.http import QueryDict
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Notepad, Note
from .forms import NotepadForm, NoteForm

import json


def index(request):
    user = User.objects.get(id=1)

    context = {'user': user}
    return render(request, 'main/index.html', context)


@csrf_exempt
def ajax_notepad(request, notepad_id=None):
    user = User.objects.get(id=1)
    if notepad_id is not None:
        notepad = Notepad.objects.get(id=notepad_id)

    # Create notepad
    if request.method == 'POST':
        data = QueryDict(request.body).dict()
        notepad = Notepad(title=data['title'], user=user)
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
        return HttpResponse(json.dumps(response), status=404, content_type="application/json")

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


@csrf_exempt
def ajax_note(request, note_id=None):
    user = User.objects.get(id=1)
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
