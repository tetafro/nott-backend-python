from django.http import JsonResponse
from django.shortcuts import render


def index(request):
    """HTML frame for JS app"""

    # Terminate non-existing API endpoints
    if request.get_full_path()[:4] == '/api':
        return JsonResponse({'error': 'not found'}, status=404)

    # Render the same page on any non-API request
    return render(request, 'index.html')
