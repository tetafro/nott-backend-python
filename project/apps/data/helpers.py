from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os


class OverwriteStorage(FileSystemStorage):
    """ Provide filename for uploads """

    def get_available_name(self, name):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name


def avatar_filename(self, filename):
    """ Filename and path for avatars """

    directory = 'avatars'
    filename = self.user.username + '.jpg'
    path = os.path.join(directory, filename)

    return path


def tree_to_list(folder, level=0):
    """ Make a tree representation of folder, subfolders and notepads """

    folder.level = level
    tree_list = [folder]
    if folder.subfolders.count():
        for subfolder in folder.subfolders.order_by('title'):
            tree_list += tree_to_list(subfolder, level+1)
    if folder.notepads.count():
        for notepad in folder.notepads.order_by('title'):
            notepad.level = level + 1
            tree_list += [notepad]

    return tree_list
