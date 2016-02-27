# Django buit-in registration form
from django.contrib.auth import forms

from .models import User


class UserCreationForm(forms.UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ('username', 'email')
