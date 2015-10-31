from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from django.conf import settings

from notes.helpers import get_client_location

import os

# Helpers
from notes.helpers import get_client_location
from .helpers import OverwriteStorage, avatar_filename


class UserProfile(models.Model):
    """
    Additional info for standard User model,
    created automaticaly by RegistrationForm
    """

    user = models.OneToOneField(User, related_name='profile')
    avatar = models.FileField(upload_to=avatar_filename,
                              storage=OverwriteStorage(),
                              blank=True,
                              null=True)

    @property
    def avatar_url(self):
        """ Check if avatar file exist and return URL """
        avatar_file = os.path.join(settings.MEDIA_ROOT, str(self.avatar))
        if self.avatar and os.path.isfile(avatar_file):
            avatar = settings.MEDIA_URL + str(self.avatar)
        else:
            avatar = settings.STATIC_URL + 'images/no-avatar.png'
        return avatar


    def save(self, *args, **kwargs):
        super(UserProfile, self).save(*args, **kwargs)

        # Resize uploaded file
        if self.avatar:
            avatar_file = os.path.join(settings.MEDIA_ROOT, str(self.avatar))
            helpers.image_resize(avatar_file, avatar_file, 180)

    def __repr__(self):
        return 'User ID%d Profile' % self.id


class UserGeo(models.Model):
    """
    Geo info for standard User model,
    created automaticaly by RegistrationForm
    """

    user = models.OneToOneField(User, related_name='geo_info')
    ip = models.CharField(max_length=15, null=True, blank=True)
    country_code = models.CharField(max_length=2, null=True, blank=True)
    country_name = models.CharField(max_length=16, null=True, blank=True)
    region_code = models.CharField(max_length=8, null=True, blank=True)
    region_name = models.CharField(max_length=32, null=True, blank=True)
    city = models.CharField(max_length=16, null=True, blank=True)
    zip_code = models.IntegerField(null=True, blank=True)
    time_zone = models.CharField(max_length=16, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    metro_code = models.IntegerField(null=True, blank=True)

    def update_geo(self, ip):
        """ Save fields from geo info remote service """
        info = get_client_location(ip)
        if 'error' in info:
            return False
        else:
            for attr in info:
                setattr(self, attr, info[attr])
            self.save()
            return True

    def __repr__(self):
        return 'User ID%d Geo Info' % self.id


class Notepad(models.Model):
    title = models.CharField(max_length=80)
    user = models.ForeignKey(User, related_name='notepads')
    parent = models.ForeignKey(
        'self',
        related_name='children',
        null=True,
        blank=True
    )

    def clean(self):
        if self.title == '':
            raise ValidationError('Title cannot be empty')
        if len(self.title) > 80:
            raise ValidationError('Title is too long')
        if not self.parent and self.parent is not None:
            raise ValidationError('This field cannot be blank')

    def __repr__(self):
        return 'Notepad ID%d' % self.id


class Note(models.Model):
    title = models.CharField(max_length=80)
    text = models.TextField(blank=True)
    notepad = models.ForeignKey(Notepad, related_name='notes')

    def clean(self):
        if self.title == '':
            raise ValidationError('Title cannot be empty')
        if len(self.title) > 80:
            raise ValidationError('Title is too long')

    def __repr__(self):
        return 'Note ID%d' % self.id
