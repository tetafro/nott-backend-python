from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^healthz$', views.healthz, name='healthz'),
]
