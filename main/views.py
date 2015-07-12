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

    context = {'title': 'Title',
        'user': user,
        'form': form
    }
    return render(request, 'main/index.html', context)


def notepad(request, notepad_id):
    user = User.objects.get(id=1)
    notepad = Notepad.objects.get(id=notepad_id)

    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.notepad = notepad
            post.save()

    form = NoteForm()

    context = {'title': 'Title',
        'user': user,
        'notepad': notepad,
        'form': form
    }
    return render(request, 'main/notepad.html', context)
