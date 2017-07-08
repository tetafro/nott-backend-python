from django.conf import settings


def add_debug(request):
    """Add DEBUG variable to every template's context"""
    return {'DEBUG': settings.DEBUG}
