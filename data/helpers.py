from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os


class OverwriteStorage(FileSystemStorage):
    """ Provide filename for uploads """

    def get_available_name(self, name):
        # Remove if already exists
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name


def avatar_filename(self, filename):
    """ Filename and path for avatars """

    directory = 'avatars'
    filename = self.user.username + '.jpg'
    path = os.path.join(directory, filename)

    return path
