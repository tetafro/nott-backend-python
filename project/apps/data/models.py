# Django
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.conf import settings

# Helper libs
import os
from pytz import timezone
from datetime import datetime

# Helpers
from notes.helpers import UpdateGeo, image_resize
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
            image_resize(avatar_file, avatar_file, 180)

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
        UpdateGeo(self, ip).start()

    @property
    def local_time(self):
        """ Get local time by timezone from geo info """
        if self.time_zone:
            tzone = timezone(self.time_zone)
            local_time = datetime.now(tzone)
        else:
            local_time = datetime.now()
        return local_time.strftime('%H:%M')

    @property
    def str_coordinates(self):
        """ Output coordinates for using in map """
        if self.latitude and self.longitude:
            info = '%s, %s' % (str(self.latitude), str(self.longitude))
        else:
            info = None
        return info

    @property
    def str_short(self):
        """ Output short geo info """
        if self.city and self.country_name:
            lat_grad = round(self.latitude)
            lon_grad = round(self.longitude)
            # First two digits of decimal part
            lat_min = str(self.latitude % 1)[2:4]
            lon_min = str(self.longitude % 1)[2:4]

            # Using %s, because %f gives a bunch of trailing zeros
            # Unicode symbols - grads and minutes
            info = u'%s, %s (%s\u00B0%s\u2032, %s\u00B0%s\u2032)' % (
                self.country_name, self.city,
                lat_grad, lat_min,
                lon_grad, lon_min)

        else:
            info = None
        return info

    @property
    def country_flag(self):
        """ Return URL for flag image or to undefined flag """

        base_url = settings.STATIC_URL + 'images/flags/'

        # Default
        flag = base_url + '_unknown.png'

        # Check if file exists
        if self.country_code:
            for directory in settings.STATICFILES_DIRS:
                filename = self.country_code.lower()+'.png'
                flag_file = os.path.join(directory, 'images', 'flags', filename)
                if os.path.isfile(flag_file):
                    flag = base_url + filename
                    break

        return flag

    def __repr__(self):
        return 'User ID%d Geo Info' % self.id


class Folder(models.Model):
    """
    Folders are containers for notepads
    Root folders (with no parents) can also contain
    other folders
    """

    title = models.CharField(max_length=80)
    user = models.ForeignKey(User, related_name='folders')
    parent = models.ForeignKey(
        'self',
        related_name='subfolders',
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
        return 'Folder ID%d' % self.id


class Notepad(models.Model):
    title = models.CharField(max_length=80)
    folder = models.ForeignKey(Folder, related_name='notepads', null=True)

    def clean(self):
        if self.title == '':
            raise ValidationError('Title cannot be empty')
        if len(self.title) > 80:
            raise ValidationError('Title is too long')

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
