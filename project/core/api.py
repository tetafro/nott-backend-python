import json

from django.http import JsonResponse as DefaultJsonResponse
from django.views.generic import View


JsonResponse404 = DefaultJsonResponse(
    {'error': 'Object not found'},
    status=404
)
JsonResponse500 = DefaultJsonResponse(
    {'error': 'Internal server error'},
    status=500
)


class JsonResponse(DefaultJsonResponse):
    def __init__(self, data, **kwargs):
        super().__init__({'data': data}, **kwargs)


class JsonErrorResponse(DefaultJsonResponse):
    def __init__(self, data, **kwargs):
        super().__init__({'error': data}, **kwargs)


class ApiView(View):
    """
    Add list method for dispatcher when id is not
    provided for the GET-method
    """

    def dispatch(self, request, *args, **kwargs):
        method = request.method.lower()

        if method == 'get' and 'id' not in self.kwargs:
            handler = getattr(self, 'list', self.http_method_not_allowed)
        elif method in self.http_method_names:
            handler = getattr(self, method, self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed

        return handler(request, *args, **kwargs)


class Serializer(object):
    """Abstract class for adding serializing functionality"""

    dict_fields = []

    def to_dict(self):
        d = {}
        for field in self.dict_fields:
            value = getattr(self, field)
            if isinstance(value, Serializer):
                d[field] = value.to_dict()
            else:
                d[field] = value
        return d


def token_required(func):
    """login_requred analog for API"""

    def wrap(request, *args, **kwargs):
        error401 = JsonResponse({'error': 'unauthorized'}, status=401)
        if 'HTTP_AUTHORIZATION' in request.META:
            if request.user is None or not request.user.is_active:
                return error401
            else:
                return func(request, *args, **kwargs)
        else:
            return error401

    return wrap


def get_token(request):
    """Get token from HTTP header"""

    if 'HTTP_AUTHORIZATION' in request.META:
        full_auth = request.META['HTTP_AUTHORIZATION'].split(' ')
        if len(full_auth) < 2 or full_auth[0] != 'Token':
            return None

        auth = full_auth[1].split('=')
        if len(auth) < 2 or auth[0] != 'token':
            return None
        token = auth[1].strip('"')
        return token
    return None


def login_test(post, email, password):
    """Sign in user for test cases and return formatted string
    with token for HTTP_AUTHORIZATION header"""

    creds = {'email': email, 'password': password}
    response = post(
        '/api/v1/login',
        content_type='application/json',
        data=json.dumps(creds)
    )
    data = json.loads(response.content.decode('utf-8'))
    return 'Token token="%s"' % data['token']
