from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^notepad/$', views.notepad_crud, name='ajax_notepad'),
    url(r'^notepad/(?P<notepad_id>\d+)/$', views.notepad_crud, name='ajax_notepad'),
    url(r'^note/$', views.note_crud, name='ajax_note'),
    url(r'^note/(?P<note_id>\d+)/$', views.note_crud, name='ajax_note'),
]
