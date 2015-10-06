from django.forms import ModelForm, FileInput
from django.contrib.auth.models import User
from .models import UserProfile


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['email']


class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar']
        widgets = {
            'avatar': FileInput(),
        }
