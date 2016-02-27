from django.conf import settings

from django.conf.urls import include, url
from django.conf.urls.static import static


urlpatterns = [
    url(r'^ajax/', include('apps.ajax.urls')),
    url(r'', include('apps.web.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
