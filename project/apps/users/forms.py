from django.contrib.auth import forms
from django.forms import ModelForm, FileInput

from .models import User


class UserCreationForm(forms.UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ('username', 'email')


# These two form is used in user profile editing
class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['email', 'avatar']
        widgets = {'avatar': FileInput(), }


# Extended registration form
class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]
