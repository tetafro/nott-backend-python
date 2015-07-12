from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^notepad/(?P<notepad_id>\d+)/$', views.notepad, name='notepad'),
    url(r'^note/(?P<note_id>\d+)/$', views.note, name='note'),
]