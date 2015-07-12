from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^notepad/(?P<notepad_id>\d+)/$', views.notepad, name='main-notepad'),
]