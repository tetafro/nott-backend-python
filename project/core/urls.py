from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static


urlpatterns = [
    url(r'^admin/', include('apps.admin.urls')),
    url(r'', include('apps.health.urls')),
    url(r'', include('apps.notes.urls')),
    url(r'', include('apps.users.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
