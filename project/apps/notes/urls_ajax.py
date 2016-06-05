from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views_ajax import FolderView, NotepadView, NoteView, SearchView

urlpatterns = [
    url(r'^folders/?$', login_required(FolderView.as_view())),
    url(r'^folders/(?P<id>\d+)/?$', login_required(FolderView.as_view())),
    url(r'^notepads/?$', login_required(NotepadView.as_view())),
    url(r'^notepads/(?P<id>\d+)/?$', login_required(NotepadView.as_view())),
    url(r'^notes/?$', login_required(NoteView.as_view())),
    url(r'^notes/(?P<id>\d+)/?$', login_required(NoteView.as_view())),
    url(r'^search/?$', login_required(SearchView.as_view())),
]
