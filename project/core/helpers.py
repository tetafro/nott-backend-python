import json

from django.http import HttpResponse
from .middleware import Http400


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
