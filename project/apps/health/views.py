from django.shortcuts import HttpResponse


def healthz(request):
    """Endpoint for service healthcheck"""
    return HttpResponse('', status=200)
