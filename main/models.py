from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

# class UserProfile(models.Model):
#     user = models.OneToOneField(User)

#     avatar = models.CharField(max_length=128, blank = True)

#     def __repr__(self):
#         return('User ID%d' % self.id)


class Notepad(models.Model):
    title = models.CharField(max_length=32)
    user = models.ForeignKey(User, related_name='notepads')
    
    def __repr__(self):
        return('Notepad ID%d' % self.id)


class Note(models.Model):
    title = models.CharField(max_length=32)
    text = models.TextField(blank = True)
    notepad = models.ForeignKey(Notepad, related_name='notes')

    def __repr__(self):
        return('Note ID%d' % self.id)
