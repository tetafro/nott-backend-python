from django.conf.urls import url

from .views import upload


urlpatterns = [
    url(r'files/?$', upload, name='upload')
]
