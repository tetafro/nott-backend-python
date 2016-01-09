from django.shortcuts import render


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
            return render(request, '400.html', status=400)
        elif isinstance(exception, Http403):
            return render(request, '403.html', status=403)
        elif isinstance(exception, Http500):
            return render(request, '500.html', status=500)
        else:
            return None
