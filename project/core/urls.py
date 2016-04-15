from django.conf.urls import include, url

urlpatterns = [
    url(r'^ajax/', include('apps.notes.urls_ajax')),
    url(r'', include('apps.notes.urls_web')),
    url(r'', include('apps.users.urls'))
]
