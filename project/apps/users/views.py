import json
import logging
import random
import string

from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models import Count
from django.utils.html import escape
from django.views.generic import View

from core.api import ApiView, get_token, \
    JsonResponse, JsonErrorResponse, JsonResponse500
from .models import BadInput, User, Token


def generate_token():
    token_length = 64
    chars = string.ascii_lowercase + \
        string.ascii_uppercase + \
        string.digits
    token = ''.join(random.choice(chars) for each in range(token_length))
    return token


class RegisterView(View):
    """Process registration requests"""

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode('utf-8'))
        email = data.get('email')
        password = data.get('password')

        if email != escape(email):
            return JsonErrorResponse('invalid characters in email', status=400)

        if not password:
            return JsonErrorResponse('password cannot be empty', status=400)

        # Create user
        # TODO: validate email format
        try:
            user = User.objects.create_user(
                email=email,
                password=password
            )
            user.save()
        except IntegrityError:
            return JsonErrorResponse('email is already taken', status=400)

        # Sign in created user
        try:
            token = Token.objects.create(
                string=generate_token(),
                user=user
            )
            token.save()
        except (IntegrityError, ValidationError) as e:
            logging.error('Failed to create token: %s', e)
            return JsonResponse500

        return JsonResponse(token.to_dict(), status=200)


class LoginView(View):
    """Process login requests"""

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode('utf-8'))
        email = data.get('email')
        password = data.get('password')

        user = authenticate(email=email, password=password)

        if user is None:
            return JsonErrorResponse('wrong email or password', status=400)

        try:
            token = Token.objects.create(string=generate_token(), user=user)
            token.save()
        except (IntegrityError, ValidationError) as e:
            logging.error('Failed to create token: %s', e)
            return JsonResponse500

        return JsonResponse(token.to_dict(), status=200)


class LogoutView(View):
    """Process logout requests"""

    def post(self, request, *args, **kwargs):
        token = get_token(request)
        try:
            token = Token.objects.get(string=token).delete()
            return JsonResponse({}, status=200)
        except Token.DoesNotExist:
            return JsonErrorResponse('invalid token', status=400)


class ProfileView(View):
    """Return current user profile"""

    def get(self, request, *args, **kwargs):
        response = request.user.to_dict()
        return JsonResponse(response, status=200)
