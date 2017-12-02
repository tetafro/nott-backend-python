from markdown2 import markdown

from django.db import models
from django.core.exceptions import ValidationError

from apps.users.models import User


class Serializer(object):
    """Abstract class for adding serializing functionality"""

    dict_fields = []

    def to_dict(self):
        return {f: getattr(self, f) for f in self.dict_fields}


class Folder(models.Model, Serializer):
    """Folder is a container for notepads or other folders"""

    title = models.CharField(max_length=80)
    user = models.ForeignKey(User, related_name='folders')
    parent = models.ForeignKey(
        'self',
        related_name='subfolders',
        null=True,
        blank=True
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    dict_fields = ['id', 'title', 'parent_id', 'created', 'updated']

    def clean(self):
        if self.title == '':
            raise ValidationError('Title cannot be empty')
        if len(self.title) > 80:
            raise ValidationError('Title is too long')

    def __repr__(self):
        return 'Folder ID%d' % self.id


class Notepad(models.Model, Serializer):
    """Notepad is a container for notes"""

    title = models.CharField(max_length=80)
    user = models.ForeignKey(User, related_name='notepads')
    folder = models.ForeignKey(Folder, related_name='notepads', null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    dict_fields = ['id', 'title', 'folder_id', 'created', 'updated']

    def clean(self):
        if self.title == '':
            raise ValidationError('Title cannot be empty')
        if len(self.title) > 80:
            raise ValidationError('Title is too long')

    def __repr__(self):
        return 'Notepad ID%d' % self.id


class Note(models.Model, Serializer):
    """Note is a container for user text data"""

    title = models.CharField(max_length=80)
    user = models.ForeignKey(User, related_name='notes')
    text = models.TextField(blank=True)  # source text in markdown
    notepad = models.ForeignKey(Notepad, related_name='notes')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    dict_fields = ['id', 'title', 'text', 'notepad_id',
                   'created', 'updated', 'html']

    def clean(self):
        if self.title == '':
            raise ValidationError('Title cannot be empty')
        if len(self.title) > 80:
            raise ValidationError('Title is too long')

    def __repr__(self):
        return 'Note ID%d' % self.id

    @property
    def html(self):
        """Convert text in mardown to HTML"""
        return markdown(self.text, extras=['fenced-code-blocks', 'tables'])
