from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^folder/$', views.folder, name='ajax_folder'),
    url(r'^folder/(?P<folder_id>\d+)/$', views.folder, name='ajax_folder'),
    url(r'^notepad/$', views.notepad, name='ajax_notepad'),
    url(r'^notepad/(?P<notepad_id>\d+)/$', views.notepad, name='ajax_notepad'),
    url(r'^note/$', views.note, name='ajax_note'),
    url(r'^note/(?P<note_id>\d+)/$', views.note, name='ajax_note'),
    url(r'^search/$', views.search, name='search'),
]
