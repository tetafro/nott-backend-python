from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^ajax/notepad/$', views.ajax_notepad, name='ajax_notepad'),
    url(r'^ajax/notepad/(?P<notepad_id>\d+)/$', views.ajax_notepad, name='ajax_notepad'),
    url(r'^ajax/note/$', views.ajax_note, name='ajax_note'),
    url(r'^ajax/note/(?P<note_id>\d+)/$', views.ajax_note, name='ajax_note'),
]