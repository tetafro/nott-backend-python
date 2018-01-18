from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static


urlpatterns = [
    url(r'^api/v1/', include('apps.admin.urls')),
    url(r'^api/v1/', include('apps.files.urls')),
    url(r'^api/v1/', include('apps.notes.urls')),
    url(r'^api/v1/', include('apps.users.urls')),
    url(r'', include('apps.health.urls')),
    url(r'', include('apps.base.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
