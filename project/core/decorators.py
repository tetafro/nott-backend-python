from django.http import JsonResponse


def login_required_ajax(view_func):
    """
    Simplified replacement for standard login_required decorator for AJAX views.
    Returns 401 (unauthorized) instead of redirection to login page.
    """

    def wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated():
            return view_func(request, *args, **kwargs)
        else:
            response = {'error': 'Unauthorized'}
            return JsonResponse(response, status=401)

    return wrapped_view
