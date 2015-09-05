#!/usr/bin/env python

import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "notes.settings")
from django.contrib.auth.models import User
from main.models import Notepad

# user = User.objects.create_user('user', 'user@nott.tk', '123')
# user = User.objects.get(id=1)
# root_notepad = Notepad(id=1, title='root', user=user)
# root_notepad.save()

users = User.objects.all()
print(users)
# notepads = Notepad.objects.all()
# print(notepads)