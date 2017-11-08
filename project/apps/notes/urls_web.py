from django.conf.urls import url
from .views_web import index


urlpatterns = [
    url(r'^$', index, name='index'),
]
