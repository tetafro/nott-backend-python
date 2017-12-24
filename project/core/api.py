from django.views.generic import View
from django.http import JsonResponse


class ApiView(View):
    """
    Add list method for dispatcher when id is not
    provided for the GET-method
    """

    # Model's fields that cannot be changed by the clients
    readonly_fields = []

    def clear_input(self, data):
        """Remove readonly fields from client's input"""
        for field in self.readonly_fields:
            if field in data:
                del data[field]

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
        error401 = JsonResponse({'error': 'Unauthorized'}, status=401)
        if 'HTTP_AUTHORIZATION' in request.META:
            if request.user is None or not request.user.is_active:
                return error401
            else:
                return func(request, *args, **kwargs)
        else:
            return error401

    return wrap