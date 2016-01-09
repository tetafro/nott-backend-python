#!/usr/bin/env python

import django
import os, sys


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "notes.settings")
from django.contrib.auth.models import User
from data.models import Folder, Notepad
django.setup()

user = User.objects.get(id=1)
# # folder_tmp = Folder(title='TEMP', user=user)
# # folder_tmp.save()
# folder_tmp = Folder.objects.get(id=1)

# all_notepads = Notepad.objects.all()
# for notepad in all_notepads:
#     notepad.folder = folder_tmp
#     notepad.save()

# print('done')




# root_folders = list(user.folders \
#                    .filter(parent_id=None) \
#                    .order_by('title') \
#                    .all())
roots = user.folders.count()
print(roots)

# def make_folder_tree(folders):
#     current_folder = folders[-1]

#     if current_folder.subfolders.count():
#         for subfolder in current_folder.subfolders:
#             folders += [subfolder]
#             make_folder_tree(folders)

#     return folders

# folders = make_folder_tree([root_folders[0]])
# print(folders)
