from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    """Main page"""
    return render(request, 'notes/index.html')
