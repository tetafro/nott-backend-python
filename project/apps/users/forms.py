from django.contrib.auth import forms
from django.forms import ModelForm, FileInput

from .models import User, UserGeo


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

    # Make profile and geo info for new user
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            geo_info = UserGeo(user=user)
            geo_info.save()

        return user
