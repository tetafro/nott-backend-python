from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


# class UserProfile(models.Model):
#     user = models.OneToOneField(User)

#     avatar = models.CharField(max_length=128, blank = True)

#     def __repr__(self):
#         return('User ID%d' % self.id)


class Notepad(models.Model):
    title = models.CharField(max_length=80)
    user = models.ForeignKey(User, related_name='notepads')
    parent = models.ForeignKey('self', related_name='children', default=1)

    def clean(self):
        if self.title == '':
            raise ValidationError('Title cannot be empty')
        if len(self.title) > 80:
            raise ValidationError('Title is too long')

    def __repr__(self):
        return('Notepad ID%d' % self.id)


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
        return('Note ID%d' % self.id)
