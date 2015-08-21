#!/usr/bin/env python
import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "notes.settings")
from django.contrib.auth.models import User

# user = User.objects.create_user('user', 'user@nott.tk', '123')

users = User.objects.all()
print(users)