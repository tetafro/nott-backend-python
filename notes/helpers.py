# Main
from django.http import HttpResponse

# HTTP exceptions
from django.http import Http404
from .middleware import Http400, Http403, Http500

# Proccessing avatars
from PIL import Image

# Getting GeoIP info
import requests


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


def csrf_failure(request, reason=''):
    """
    Custom error for missing CSRF token
    """

    # Don't tell user anything!
    if request.get_full_path()[:5] == '/ajax':
        response = {'error': 'Please refresh the page'}
        return HttpResponse(json.dumps(response), status=400)
    else:
        raise Http400()


def get_client_ip(request):
    """
    Get client's IP
    """

    real_ip = request.META.get('HTTP_X_REAL_IP')
    # Proxy
    if real_ip:
        ip = real_ip
    # No proxy
    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip


def get_client_location(ip):
    """
    Get client's geo info in JSON
    Sample:
        ip: 10.10.10.10,
        country_code: XX,
        country_name: Country,
        region_code: YYY,
        region_name: State name,
        city: City,
        zip_code: 123456,
        time_zone: Region/Zone,
        latitude: 10.123,
        longitude: 10.123,
        metro_code: 0
    """

    # TODO: remove after testing
    ip = '128.70.126.226'
    result = {}
    try:
        response = requests.get('http://freegeoip.net/json/'+ip)
    except ConnectionError:
        result['error'] = 'Connection error'
    except Timeout:
        result['error'] = 'Connection timeout'
    except HTTPError:
        result['error'] = 'Invalid response'
    else:
        if response.status_code == 200:
            json = response.json()
            if not 'latitude' in json and not 'longitude' in json:
                result['error'] = 'No geo info available'
            else:
                result = json
        else:
            result['error'] = 'Bad request'

    return result
