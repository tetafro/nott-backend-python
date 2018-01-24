from markdown2 import markdown

from django.core.exceptions import ValidationError
from django.db import models, IntegrityError
from django.utils.html import escape

from core.api import Serializer
from apps.users.models import User


class BadInput(Exception):
    """Used when model is saving to indicate problems with it's fields"""
    pass


class Folder(models.Model, Serializer):
    """Folder is a container for notepads or other folders"""

    title = models.CharField(max_length=80)
    user = models.ForeignKey(
        User,
        related_name='folders',
        on_delete=models.CASCADE
    )
    parent = models.ForeignKey(
        'self',
        related_name='subfolders',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    # Fields to be given to clients
    dict_fields = ['id', 'title', 'parent_id', 'created', 'updated']

    def clean(self):
        if self.title == '':
            raise ValidationError('title cannot be empty')
        if len(self.title) > 80:
            raise ValidationError('title is too long')

    def full_save(self):
        try:
            self.full_clean()
        except ValidationError as e:
            raise BadInput(', '.join(e.messages))
        try:
            self.save()
        except IntegrityError:
            raise BadInput('failed to save the object')

    def __repr__(self):
        return 'Folder ID%d' % self.id


class Notepad(models.Model, Serializer):
    """Notepad is a container for notes"""

    title = models.CharField(max_length=80)
    user = models.ForeignKey(
        User,
        related_name='notepads',
        on_delete=models.CASCADE
    )
    folder = models.ForeignKey(
        Folder,
        related_name='notepads',
        null=True,
        on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    # Fields to be given to clients
    dict_fields = ['id', 'title', 'folder_id', 'created', 'updated']

    def clean(self):
        if self.title == '':
            raise ValidationError('title cannot be empty')
        if len(self.title) > 80:
            raise ValidationError('title is too long')

    def full_save(self):
        try:
            self.full_clean()
        except ValidationError as e:
            raise BadInput(', '.join(e.messages))
        try:
            self.save()
        except IntegrityError:
            raise BadInput('failed to save the object')

    def __repr__(self):
        return 'Notepad ID%d' % self.id


class Note(models.Model, Serializer):
    """Note is a container for user text data"""

    title = models.CharField(max_length=80)
    user = models.ForeignKey(
        User,
        related_name='notes',
        on_delete=models.CASCADE
    )
    text = models.TextField(blank=True)  # source text in markdown
    notepad = models.ForeignKey(
        Notepad,
        related_name='notes',
        on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    # Fields to be given to clients
    dict_fields = ['id', 'title', 'text', 'html', 'notepad_id',
                   'created', 'updated']

    def clean(self):
        if self.title == '':
            raise ValidationError('title cannot be empty')
        if len(self.title) > 80:
            raise ValidationError('title is too long')

    def full_save(self):
        try:
            self.full_clean()
        except ValidationError as e:
            raise BadInput(', '.join(e.messages))
        try:
            self.save()
        except IntegrityError:
            raise BadInput('failed to save the object')

    def __repr__(self):
        return 'Note ID%d' % self.id

    @property
    def html(self):
        """Convert text in mardown to HTML"""
        return markdown(
            self.text,
            extras=['fenced-code-blocks', 'tables', 'header-ids'],
            safe_mode='escape'
        )
