from django.db import models
from django.core.exceptions import ValidationError

from apps.users.models import User


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
