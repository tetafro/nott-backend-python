import os
import uuid
from PIL import Image

from django.conf import settings
from django.core.files.base import ContentFile
from django.http import JsonResponse

from core.api import JsonResponse405, JsonResponse500


def image_resize(img_input, img_output, max_size):
    """Resize input image so that longest side is equal to max_size"""

    # Read file
    image = Image.open(img_input).convert('RGB')
    image_size = image.size

    # Resize
    ratio = max_size / max(image_size[0], image_size[1])
    new_size = (int(image_size[0] * ratio), int(image_size[1] * ratio))
    image = image.resize(new_size, Image.ANTIALIAS)

    # Save to disk
    image.save(img_output, format='JPEG')


def upload(request):
    """Upload binary file"""

    if request.method != 'POST':
        return JsonResponse405

    uploaded_file = request.FILES.get('file')
    if not uploaded_file:
        error = {'error': 'request has no file'}
        return JsonResponse(error, status=400)

    file_content = ContentFile(uploaded_file.read())

    # Check if it is a valid image
    try:
        img = Image.open(file_content)
        fmt = img.format.lower()
        img.close()
    except (OSError, IOError):
        error = {'error': 'the file is not a valid image'}
        return JsonResponse(error, status=400)

    # Save to disk
    name = str(uuid.uuid4()) + '.' + fmt
    file_path = os.path.join(settings.MEDIA_ROOT, name)
    try:
        with open(file_path, 'wb+') as f:
            for chunk in file_content.chunks():
                f.write(chunk)
    except FileNotFoundError:
        return JsonResponse500

    # Resize
    image_resize(file_path, file_path, 180)

    url = settings.MEDIA_URL + name
    return JsonResponse({'url': url}, status=200)
