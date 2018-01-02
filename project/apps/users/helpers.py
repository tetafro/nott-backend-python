import os
import random
import string
from PIL import Image

from django.core.files.storage import FileSystemStorage
from django.conf import settings


class OverwriteStorage(FileSystemStorage):
    """ Provide filename for uploads """

    def __init__(self, *args, **kwargs):
        super().__init__(*args,
                         location=settings.AVATARS_ROOT,
                         **kwargs)

    def get_available_name(self, name):
        if self.exists(name):
            os.remove(os.path.join(settings.AVATARS_ROOT, name))
        return name


def image_resize(img_input, img_output, max_size):
    """
    Resizes input image so that longest side is equal to max_size
    img_input, img_output - pathes for input and output files
    max_size - length in pixels
    """

    # Read file
    image = Image.open(img_input).convert('RGB')
    image_size = image.size

    # Resize
    ratio = max_size / max(image_size[0], image_size[1])
    new_size = (int(image_size[0]*ratio), int(image_size[1]*ratio))
    image = image.resize(new_size, Image.ANTIALIAS)

    # Save to disk
    image.save(img_output, format='JPEG')

    return image


def generate_token():
    token_length = 64
    chars = string.ascii_lowercase + \
            string.ascii_uppercase + \
            string.digits
    token = ''.join(random.choice(chars) for each in range(token_length))
    return token
