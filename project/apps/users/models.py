import os
from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.conf import settings
from django.utils import timezone

from .helpers import OverwriteStorage, UpdateGeo, \
    avatar_filename, image_resize


class UserManager(BaseUserManager):
    def create_user(self, username, email, password):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            is_active=True)
        user.set_password(password)
        user.save(using=self._db)

        return user


class User(AbstractBaseUser):
    """
    Custom user model
    """

    username = models.CharField(max_length=40, unique=True)
    email = models.CharField(max_length=40, unique=True)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'username'

    # This is only for createsuperuser command
    # Username and password should not be here,
    # they are always required
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def get_full_name(self):
        return self.username
    def get_short_name(self):
        return self.username

    # Note: this can't be lamba, otherwise makemigration
    # will give an error
    def upload_to(u, f):
        return u.username

    avatar = models.FileField(upload_to=upload_to,
                              storage=OverwriteStorage(),
                              blank=True,
                              null=True)

    @property
    def avatar_url(self):
        """ Check if avatar file exist and return URL """
        avatar_file = os.path.join(settings.AVATARS_ROOT, str(self.avatar))
        if self.avatar and os.path.isfile(avatar_file):
            avatar = settings.AVATARS_URL + str(self.avatar)
        else:
            avatar = settings.STATIC_URL + 'images/no-avatar.png'
        return avatar

    # def save(self, *args, **kwargs):
    #     # Resize uploaded file
    #     if self.avatar:
    #         avatar_file = os.path.join(settings.AVATARS_ROOT, str(self.avatar))
    #         image_resize(avatar_file, avatar_file, 180)
    #     super().save(*args, **kwargs)

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
