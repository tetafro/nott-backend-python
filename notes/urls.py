from django.conf import settings

from django.conf.urls import include, url
from django.conf.urls.static import static

from django.contrib import admin


urlpatterns = [
    url(r'', include('main.urls')),
    url(r'^admin/', include(admin.site.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
