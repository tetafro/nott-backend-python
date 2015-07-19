from django.db import models


class User(models.Model):
    name = models.CharField(max_length=32)
    password = models.CharField(max_length=128)
    avatar = models.CharField(max_length=128, blank = True)
    reg_date = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return('User ID%d' % self.id)


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
