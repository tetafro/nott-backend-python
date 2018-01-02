from django.contrib.auth import authenticate

from .api import get_token


class DisableCSRFForAPI(object):
    """Disable CSRF for URLs that starts with /api/"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.get_full_path()[:4] == '/api':
            setattr(request, '_dont_enforce_csrf_checks', True)
        response = self.get_response(request)
        return response


class AuthAPI(object):
    """
    Add user to request var for API calls
    Header format (RFC2617):
    Authorization: Token token="abcd1234"
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.get_full_path()[:4] != '/api':
            return self.get_response(request)

        token = get_token(request)
        if token:
            user = authenticate(token=token)
            if user and user.is_active:
                user.backend = 'core.backends.TokenBackend'
                request.user = user

        return self.get_response(request)
