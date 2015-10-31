from django.forms import ModelForm, FileInput
from django.contrib.auth.models import User
from data.models import UserProfile, UserGeo

# Django buit-in registration form
from django.contrib.auth.forms import UserCreationForm


# These two form is used in user profile editing
class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['email']


class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar']
        widgets = {'avatar': FileInput(),}


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
        user = super(RegistrationForm, self).save(commit=False)
        if commit:
            user.save()
            profile = UserProfile(user=user)
            profile.save()
            geo_info = UserGeo(user=user)
            geo_info.save()

        return user
