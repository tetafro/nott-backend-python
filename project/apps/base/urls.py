from django.conf.urls import url

from .views import index


urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^login/?$', index, name='index'),
    url(r'^register/?$', index, name='index'),
    url(r'^logout/?$', index, name='index'),
    url(r'^admin/?$', index, name='index'),
    url(r'^users/?$', index, name='index'),
    url(r'^users/me/?$', index, name='index'),
    url(r'^users/\d+/?$', index, name='index'),
]
