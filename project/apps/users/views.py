import json
import logging

from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models import Count
from django.http import JsonResponse
from django.utils.html import escape
from django.views.generic import View

from core.api import ApiView, get_token
from apps.admin.models import Config
from .models import BadInput, User, Token
from .helpers import generate_token


class LoginView(View):
    """Process login requests"""

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode('utf-8'))
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)

        if user is None:
            response = {'error': 'wrong username or password'}
            return JsonResponse(response, status=400)

        try:
            token = Token.objects.create(string=generate_token(), user=user)
            token.save()
        except (IntegrityError, ValidationError) as e:
            logging.error('Failed to create token: %s', e)
            return JsonResponse({}, status=500)

        return JsonResponse({'token': token.string}, status=200)


class RegisterView(View):
    """Process registration requests"""

    def post(self, request, *args, **kwargs):
        try:
            db_setting = Config.objects.get(code='allow_registration')
        except Config.DoesNotExist:
            reg_allowed = True  # default if settings is not found
        else:
            reg_allowed = db_setting.value == 'true'

        if not reg_allowed:
            response = {'error': 'registration is currently disabled'}
            return JsonResponse(response, status=400)

        data = json.loads(request.body.decode('utf-8'))
        username = data.get('username')
        email = data.get('email')
        password1 = data.get('password1')
        password2 = data.get('password2')

        if username != escape(username):
            response = {'error': 'invalid characters in username'}
            return JsonResponse(response, status=400)

        if email != escape(email):
            response = {'error': 'invalid characters in email'}
            return JsonResponse(response, status=400)

        if password1 != password2:
            response = {'error': 'passwords do not match'}
            return JsonResponse(response, status=400)

        # Create user
        # TODO: validate email format
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1
            )
            user.save()
        except IntegrityError:
            response = {'error': 'username or email is already taken'}
            return JsonResponse(response, status=400)

        # Sign in created user
        try:
            token = Token.objects.create(
                string=generate_token(),
                user=user
            )
            token.save()
        except (IntegrityError, ValidationError) as e:
            logging.error('Failed to create token: %s', e)
            return JsonResponse({}, status=500)

        return JsonResponse({'token': token.string}, status=200)


class LogoutView(View):
    """Process logout requests"""

    def post(self, request, *args, **kwargs):
        token = get_token(request)
        print(token)
        try:
            Token.objects.get(string=token).delete()
            return JsonResponse({}, status=200)
        except Token.DoesNotExist:
            return JsonResponse({'error': 'invalid token'}, status=400)


class UserView(ApiView):
    """Full CRUD for User model"""

    editable_fields = ['email']

    def list(self, request, *args, **kwargs):
        users = User.objects.\
            annotate(folders_count=Count(
                'folders',
                distinct=True
            )).\
            annotate(notepads_count=Count(
                'folders__notepads',
                distinct=True
            )).\
            annotate(notes_count=Count(
                'folders__notepads__notes',
                distinct=True
            )).\
            all()
        response = {'users': [u.to_dict() for u in users]}
        return JsonResponse(response)

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        try:
            # Get user's stats
            user = User.objects.\
                annotate(folders_count=Count(
                    'folders',
                    distinct=True
                )).\
                annotate(notepads_count=Count(
                    'folders__notepads',
                    distinct=True
                )).\
                annotate(notes_count=Count(
                    'folders__notepads__notes',
                    distinct=True
                )).\
                get(id=user_id)
        except User.DoesNotExist:
            response = {'error': 'Object not found'}
            return JsonResponse(response, status=404)

        response = user.to_dict()
        return JsonResponse(response, status=200)

    def put(self, request, *args, **kwargs):
        user_id = kwargs.get('id')

        # User can modify only his own profile
        if user_id != str(request.user.id):
            return JsonResponse({'error': 'forbidden'}, status=403)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            response = {'error': 'Object not found'}
            return JsonResponse(response, status=404)

        data = json.loads(request.body.decode('utf-8'))

        for (key, value) in data.items():
            if key in self.editable_fields:
                setattr(user, key, value)

        try:
            user.full_save()
        except BadInput as e:
            response = {'error': str(e)}
            return JsonResponse(response, status=400)

        response = user.to_dict()
        return JsonResponse(response, status=200)


class ProfileView(View):
    """Return current user profile"""

    def get(self, request, *args, **kwargs):
        response = request.user.to_dict()
        return JsonResponse(response, status=200)
