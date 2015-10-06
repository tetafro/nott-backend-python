# Main
from django.shortcuts import render, redirect

# Validation exceptions
# TODO: user these
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.db import IntegrityError

# Auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Models
from django.contrib.auth.models import User
from data.models import Notepad, Note

# Forms
from data.forms import UserForm, UserProfileForm


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
    root_notepads = list(
        request.user.notepads \
                    .filter(parent_id=1) \
                    .exclude(id=1) \
                    .order_by('title')
    )
    notepads = []

    for notepad in root_notepads:
        notepads += [notepad]
        if notepad.children.count():
            notepads += list(notepad.children.order_by('title'))

    context = {'notepads': notepads}
    return render(request, 'web/index.html', context)


@login_required
def userlist(request):
    users = User.objects.all()
    # Attach notepads and notes count for each user
    for user in users:
        user.notepads_count = user.notepads.count()
        user.notes_count = User.objects \
                               .filter(notepads__notes__isnull=False) \
                               .count()

    context = {'users': users}
    return render(request, 'web/userlist.html', context)


@login_required
def profile(request, user_id):
    # TODO: make possible to view any user
    user = request.user
    # Attach notepads and notes count for the user
    user.notepads_count = user.notepads.count()
    user.notes_count = User.objects \
                           .filter(notepads__notes__isnull=False) \
                           .count()

    context = {}
    return render(request, 'web/profile.html', context)


@login_required
def profile_edit(request, user_id):
    if int(user_id) != request.user.id:
        # TODO: display forbidden error
        return redirect('profile', user_id=user_id)

    user = request.user
    # Attach notepads and notes count for the user
    user.notepads_count = user.notepads.count()
    user.notes_count = User.objects \
                           .filter(notepads__notes__isnull=False) \
                           .count()

    if request.method == 'POST':
        form_user = UserForm(request.POST, instance=user)
        form_profile = UserProfileForm(request.POST,
                                       request.FILES,
                                       instance=user.profile)

        if form_user.is_valid() and form_profile.is_valid():
            form_user.save()
            form_profile.save()
        else:
            # TODO: return error
            pass
            
    form_user = UserForm(instance=user)
    form_profile = UserProfileForm(instance=user.profile)

    context = {
        'form_user': form_user,
        'form_profile': form_profile
    }
    return render(request, 'web/profile_edit.html', context)
