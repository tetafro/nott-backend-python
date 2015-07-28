from django.core.serializers import serialize
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Notepad, Note
from .forms import NotepadForm, NoteForm

import json


def index(request):
    user = User.objects.get(id=1)
    
    if request.method == 'POST':
        if 'notepad' in request.POST:
            form = NotepadForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.user = user
                post.save()

    form_notepad = NotepadForm()
    form_note = NoteForm()

    context = {'user': user,
        'form_notepad': form_notepad,
        'form_note': form_note,
        'current_notepad': '',
        'current_note': ''
    }
    return render(request, 'main/root.html', context)


def notepad(request, notepad_id):
    user = User.objects.get(id=1)
    notepad = Notepad.objects.get(id=notepad_id)

    if request.method == 'POST':
        if 'notepad' in request.POST:
            form = NotepadForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.user = user
                post.save()
            else:
                print('not valid pad')
        elif 'note' in request.POST:
            form = NoteForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.user = user
                post.notepad = notepad
                post.save()
            else:
                print('not valid note')

    form_notepad = NotepadForm()
    form_note = NoteForm()

    context = {'user': user,
        'form_notepad': form_notepad,
        'form_note': form_note,
        'current_notepad': notepad,
        'current_note': ''
    }
    return render(request, 'main/notepad.html', context)


def note(request, note_id):
    user = User.objects.get(id=1)
    note = Note.objects.get(id=note_id)
    notepad = note.notepad

    if request.method == 'POST':
        text = request.POST.dict()['text']
        note.text = text
        note.save()
        return HttpResponse(json.dumps({'status': 'success'}))

    form_notepad = NotepadForm()
    form_note_add = NoteForm()
    form_note_update = NoteForm(initial={'title': note.title})

    context = {'user': user,
        'form_notepad': form_notepad,
        'form_note_add': form_note_add,
        'form_note_update': form_note_update,
        'current_notepad': notepad,
        'current_note': note
    }
    return render(request, 'main/note.html', context)


@csrf_exempt
def ajax_notepad(request, notepad_id=None):
    user = User.objects.get(id=1)
    if notepad_id is not None:
        notepad = Notepad.objects.get(id=notepad_id)

    # Создать блокнот
    if request.method == 'POST':
        post_data = request.POST.dict()
        notepad = Notepad(title=post_data['title'], user=user)
        notepad.save()

        respone = {'status': 'success'}
        return HttpResponse(json.dumps(respone), content_type="application/json")

    # Получить JSON со всеми блокнотами
    if request.method == 'GET':
        notepads = user.notepads.all()

        respone = {'status': 'success',
            'notepads': serialize('json', notepads)}
        return HttpResponse(json.dumps(respone), content_type="application/json")

    # Удалить блокнот
    if request.method == 'DELETE':
        notepad.delete()

        response = {'status': 'success'}
        return HttpResponse(json.dumps(response), content_type="application/json")


@csrf_exempt
def ajax_note(request, note_id):
    note = Note.objects.get(id=note_id)

    if request.method == 'DELETE':
        note.delete()
        return HttpResponse(json.dumps({'status': 'success'}))
