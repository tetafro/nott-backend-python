from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^notepad/$', views.ajax_notepad, name='ajax_notepad'),
    url(r'^notepad/(?P<notepad_id>\d+)/$', views.ajax_notepad, name='ajax_notepad'),
    url(r'^note/$', views.ajax_note, name='ajax_note'),
    url(r'^note/(?P<note_id>\d+)/$', views.ajax_note, name='ajax_note'),
]
