from django import forms
from .models import User, Notepad, Note


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'password', 'avatar']


class NotepadForm(forms.ModelForm):
    class Meta:
        model = Notepad
        fields = ['title']


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'text']