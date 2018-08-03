from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static


urlpatterns = [
    url(r'^api/v1/', include('apps.notes.urls')),
    url(r'^api/v1/', include('apps.users.urls')),
    url(r'', include('apps.health.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
