from apps.users.models import User, Token


class TokenBackend(object):
    """Token authentication for API"""

    def authenticate(self, token=None):
        try:
            t = Token.objects.get(string=token)
            return t.user
        except Token.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
