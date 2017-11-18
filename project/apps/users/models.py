import os

from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.conf import settings
from django.utils import timezone

from .helpers import OverwriteStorage, image_resize


ADMIN_ROLE_ID = 1
USER_ROLE_ID = 2


class Role(models.Model):
    """
    User roles
    """

    name = models.CharField(max_length=40, unique=True)


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
    role = models.ForeignKey(Role, default=USER_ROLE_ID)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True, null=True)
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

    @property
    def is_admin(self):
        return self.role_id == ADMIN_ROLE_ID

    # Note: this can't be lamba, otherwise makemigration
    # will give an error
    def _upload_to(u, f):
        return u.username

    avatar = models.FileField(upload_to=_upload_to,
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

    def save(self, *args, **kwargs):
        # Resize uploaded file
        if self.avatar:
            avatar_file = os.path.join(settings.AVATARS_ROOT, str(self.avatar))
            image_resize(avatar_file, avatar_file, 180)
        super().save(*args, **kwargs)

    def __repr__(self):
        return 'User ID%d Profile' % self.id
