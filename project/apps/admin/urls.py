from django.conf.urls import url

from core.api import admin_required
from .views import VersionView, SettingView


urlpatterns = [
    url(r'^version/?$', admin_required(VersionView.as_view())),
    url(r'^settings/?$', admin_required(SettingView.as_view())),
]
