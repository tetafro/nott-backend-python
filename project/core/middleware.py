import logging
import json

from django.shortcuts import render
from django.http import HttpResponse

from .errors import Http400, Http403, Http404, Http500


# Get an instance of a logger
logger = logging.getLogger(__name__)


class HttpErrorsMiddleware(object):
    """
    Catch exceptions and display custom error page
    """
    def process_exception(self, request, exception):
        if isinstance(exception, Http400):
            logger.exception('Bad request error: '+str(exception))
            return render(request, '400.html', status=400)
        elif isinstance(exception, Http403):
            logger.exception('Forbidden error: '+str(exception))
            return render(request, '403.html', status=403)
        elif isinstance(exception, Http404):
            logger.exception('Forbidden error: ' + str(exception))
            return render(request, '404.html', status=404)
        elif isinstance(exception, Http500):
            logger.exception('Internal server error: '+str(exception))
            return render(request, '500.html', status=500)
        else:
            logger.exception('Unexpected exception: '+str(exception))
            return render(request, '500.html', status=500)


def csrf_failure(request, reason=''):
    """
    Custom error for missing CSRF token
    NOTE: Django security logs this
    """

    if request.get_full_path()[:5] == '/ajax':
        response = {'error': 'Please refresh the page'}
        return HttpResponse(json.dumps(response), status=400)
    else:
        return render(request, '500.html', status=500)
