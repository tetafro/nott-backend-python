from django.shortcuts import render

from .models import User, Notepad, Note
from .forms import NotepadForm, NoteForm


def index(request):
    user = User.objects.get(id=1)
    
    if request.method == 'POST':
        form = NotepadForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = user
            post.save()

    form = NotepadForm()

    context = {'user': user,
        'form': form,
        'current_notepad': '',
        'current_note': ''
    }
    return render(request, 'main/root.html', context)


def notepad(request, notepad_id):
    user = User.objects.get(id=1)
    notepad = Notepad.objects.get(id=notepad_id)

    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = user
            post.notepad = notepad
            post.save()

    form = NoteForm()

    context = {'user': user,
        'form': form,
        'current_notepad': notepad,
        'current_note': ''
    }
    return render(request, 'main/notepad.html', context)


def note(request, note_id):
    user = User.objects.get(id=1)
    note = Note.objects.get(id=note_id)
    notepad = note.notepad

    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = user
            post.save()

    form = NoteForm(initial={'title': note.title,
        'text': note.text})

    context = {'user': user,
        'form': form,
        'current_notepad': notepad,
        'current_note': note,
        'notepads': user.notepads.all,
        'notes': note
    }
    return render(request, 'main/note.html', context)
