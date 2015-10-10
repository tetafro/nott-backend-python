from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from django.conf import settings

import os

# Helpers
from notes import helpers
from .helpers import OverwriteStorage, avatar_filename


class UserProfile(models.Model):
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
            avatar = settings.STATIC_URL + 'images/no_avatar.png'
        return avatar


    def save(self, *args, **kwargs):
        super(UserProfile, self).save(*args, **kwargs)

        # Resize uploaded file
        if self.avatar:
            avatar_file = os.path.join(settings.MEDIA_ROOT, str(self.avatar))
            helpers.image_resize(avatar_file, avatar_file, 180)

    def __repr__(self):
        return 'User ID%d' % self.id


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
