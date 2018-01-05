from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.generic import View

from core.api import ApiView
from .models import Setting


class VersionView(View):
    @method_decorator(user_passes_test(lambda u: u.is_admin))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        response = {'version': settings.VERSION}
        return JsonResponse(response, status=200)


class SettingView(ApiView):
    def list(self, request, *args, **kwargs):
        sets = Setting.objects.all()
        response = {'settings': [s.to_dict() for s in sets]}
        return JsonResponse(response)

    def get(self, request, *args, **kwargs):
        setting_id = kwargs.get('id')
        try:
            setting = Setting.objects.get(id=setting_id)
        except Setting.DoesNotExist:
            response = {'error': 'object not found'}
            return JsonResponse(response, status=404)

        response = setting.to_dict()
        return JsonResponse(response, status=200)
