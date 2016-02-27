from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views
from .views import FolderView, NotepadView, NoteView, SearchView

urlpatterns = [
    url(r'^folder/$', login_required(FolderView.as_view())),
    url(r'^folder/(?P<folder_id>\d+)/$', login_required(FolderView.as_view())),
    url(r'^notepad/$', NotepadView.as_view()),
    url(r'^notepad/(?P<notepad_id>\d+)/$', login_required(NotepadView.as_view())),
    url(r'^note/$', login_required(NoteView.as_view())),
    url(r'^note/(?P<note_id>\d+)/$', login_required(NoteView.as_view())),
    url(r'^search/$', login_required(SearchView.as_view())),
]
