from django.http import JsonResponse
from django.shortcuts import HttpResponse


def healthz(request):
    """Endpoint for service healthcheck"""
    if request.method != 'GET':
        JsonResponse({'error': 'method not allowed'}, status=405)
    return HttpResponse('', status=200)
