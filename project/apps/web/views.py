# Main
from django.shortcuts import render, redirect
from django.http import HttpResponse

# Validation exceptions
# TODO: use these
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.db import IntegrityError

# Auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Models
# from django.contrib.auth.models import User
from apps.data.models import User, UserGeo, Folder, Notepad, Note
from django.db.models import Count

# Forms
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserForm, RegistrationForm

# Helpers
from core.helpers import get_ip
from apps.data.helpers import tree_to_list


def user_auth(request):
    """
    Register or login
    """

    reg_form = RegistrationForm()
    login_form = AuthenticationForm()

    if request.method == 'POST':
        is_reg = request.POST.get('reg')

        errors = False

        # Registration
        if is_reg:
            reg_form = RegistrationForm(request.POST)
            if reg_form.is_valid():
                reg_form.save()
                user = authenticate(
                    username=reg_form.cleaned_data['username'],
                    password=reg_form.cleaned_data['password1']  # password2 - confirmation
                )
                login(request, user)
            else:
                errors = True
        # Login
        else:
            # This form has different design, so we need to
            # specify data argument explicitly
            login_form = AuthenticationForm(data=request.POST)
            if login_form.is_valid():
                login(request, login_form.get_user())
                # Fetch geo info and save it
                ip = get_ip(request)
                request.user.geo_info.update_geo(ip)
            else:
                errors = True

        # Success
        # Errors' texts are generated by forms
        if not errors:
            return redirect('index')

    context = {
        'reg_form': reg_form,
        'login_form': login_form
    }
    return render(request, 'web/auth.html', context)


@login_required
def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
def index(request):
    root_folders = request.user.folders \
                               .filter(parent_id=None) \
                               .order_by('title')

    # Folders and notepads
    items = []
    for folder in root_folders:
        items += tree_to_list(folder)

    context = {'items': items}
    return render(request, 'web/index.html', context)


@login_required
def userlist(request):
    # Get users with stats
    users = User.objects.annotate(folders_count=Count('folders', distinct=True)) \
                            .annotate(notepads_count=Count('folders__notepads', distinct=True)) \
                            .annotate(notes_count=Count('folders__notepads__notes', distinct=True)) \
                            .all()

    context = {'users': users}
    return render(request, 'web/userlist.html', context)


@login_required
def profile(request, user_id):
    if user_id == 'me' or request.user.id == int(user_id):
        user_id = request.user.id
        is_me = True
    else:
        is_me = False

    # Get user's stats
    user = User.objects.annotate(folders_count=Count('folders', distinct=True)) \
                       .annotate(notepads_count=Count('folders__notepads', distinct=True)) \
                       .annotate(notes_count=Count('folders__notepads__notes', distinct=True)) \
                       .get(id=user_id)

    context = {
        'is_me': is_me,
        'usercard': user
    }
    return render(request, 'web/profile.html', context)


@login_required
def profile_edit(request):
    # Get user's stats
    user = User.objects.annotate(folders_count=Count('folders', distinct=True)) \
                       .annotate(notepads_count=Count('folders__notepads', distinct=True)) \
                       .annotate(notes_count=Count('folders__notepads__notes', distinct=True)) \
                       .get(id=request.user.id)

    if request.method == 'POST':
        form_user = UserForm(request.POST, request.FILES, instance=user)

        if form_user.is_valid():
            form_user.save()
        else:
            # TODO: return error
            pass

        return redirect('profile', user_id='me')

    form_user = UserForm(instance=user)

    context = {
        'usercard': user,
        'form_user': form_user
    }
    return render(request, 'web/profile_edit.html', context)
