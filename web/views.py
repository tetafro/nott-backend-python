# Main
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Validation exceptions
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.db import IntegrityError

# Auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Models
from django.contrib.auth.models import User
from data.models import Notepad, Note


def user_auth(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        # Register or login
        is_reg = request.POST.get('reg')

        error_message = ''

        print(username)
        print(password)

        # Registration
        if is_reg:
            try:
                User.objects.create_user(username, email, password)
            except:
                error_message = 'Registration error'
            else:
                user = authenticate(username=username, password=password)
                login(request, user)
        # Login
        else:
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                else:
                    error_message = 'Account is blocked'
            else:
                error_message = 'Wrong username or password'

        # Fail
        if error_message:
            return redirect('login')
        # Success
        else:
            return redirect('index')

    context = {}
    return render(request, 'web/auth.html', context)


@login_required
def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
def index(request):
    root_notepads = list(request.user.notepads
        .filter(parent_id=1)
        .exclude(id=1)
        .order_by('title')
    )
    notepads = []

    for notepad in root_notepads:
        notepads += [notepad]
        if notepad.children:
            notepads += list(notepad.children.order_by('title'))

    context = {'notepads': notepads}
    return render(request, 'web/index.html', context)


@login_required
def userlist(request):
    users = User.objects.all()

    context = {'users': users}
    return render(request, 'web/userlist.html', context)
