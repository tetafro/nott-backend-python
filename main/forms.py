from django import forms
from django.contrib.auth.models import User
from .models import Notepad, Note


class UserRegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class UserLoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class NotepadForm(forms.ModelForm):
    class Meta:
        model = Notepad
        fields = ['title']


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'text']
