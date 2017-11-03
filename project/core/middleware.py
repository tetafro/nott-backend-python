import logging

from django.shortcuts import render


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Classes for HTTP errors
class Http400(Exception):
    pass


class Http403(Exception):
    pass


class Http500(Exception):
    pass


class HttpErrorsMiddleware(object):
    """
    Catch exceptions and display custom error page
    """
    def process_exception(self, request, exception):
        if isinstance(exception, Http400):
            logger.exception('Bad request error')
            return render(request, '400.html', status=400)
        elif isinstance(exception, Http403):
            logger.exception('Forbidden error')
            return render(request, '403.html', status=403)
        elif isinstance(exception, Http500):
            logger.exception('Internal server error')
            return render(request, '500.html', status=500)
        else:
            return None
