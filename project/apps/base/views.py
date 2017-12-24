from django.shortcuts import render


def index(request):
    """HTML frame for JS app"""
    return render(request, 'index.html')
