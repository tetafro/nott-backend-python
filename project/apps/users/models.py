import datetime

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.db import models, IntegrityError
from django.utils import timezone

from core.api import Serializer


class BadInput(Exception):
    """Used when model is saving to indicate problems with it's fields"""
    pass


class UserManager(BaseUserManager):
    """Helper class for managing User objects"""

    def create_user(self, email, password):
        if not email:
            raise ValueError('users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            is_active=True)
        user.set_password(password)
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, Serializer):
    """Custom user model"""

    email = models.CharField(max_length=40, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    is_active = models.BooleanField(default=True)

    # Fields to be given to clients
    dict_fields = ['id', 'email', 'created_at', 'updated_at']

    USERNAME_FIELD = 'email'

    # This is only for createsuperuser command
    # Username and password fields should not be here,
    # they are always required
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def full_save(self):
        """Validate before saving"""
        try:
            self.full_clean()
        except ValidationError as e:
            raise BadInput(', '.join(e.messages))
        try:
            self.save()
        except IntegrityError:
            raise BadInput('failed to save the object')

    def __repr__(self):
        return 'User ID%d Profile' % self.id


class Token(models.Model, Serializer):
    """Authentication token for user model"""

    # Secret string
    string = models.CharField(max_length=64, unique=True)
    # Time to live - number of seconds until token expiration
    ttl = models.IntegerField(default=3600)
    user = models.ForeignKey(
        User,
        related_name='tokens',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(default=timezone.now)

    # Fields to be given to clients
    dict_fields = ['string', 'ttl']

    @property
    def is_expired(self):
        elapsed = datetime.datetime.now() - self.created_at
        if elapsed > datetime.timedelta(seconds=self.ttl):
            return True
