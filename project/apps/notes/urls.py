from django.conf.urls import url

from core.api import token_required
from .views import FolderView, NotepadView, NoteView, SearchView


urlpatterns = [
    url(r'^folders/?$', token_required(FolderView.as_view())),
    url(r'^folders/(?P<id>\d+)/?$', token_required(FolderView.as_view())),
    url(r'^notepads/?$', token_required(NotepadView.as_view())),
    url(r'^notepads/(?P<id>\d+)/?$', token_required(NotepadView.as_view())),
    url(r'^notes/?$', token_required(NoteView.as_view())),
    url(r'^notes/(?P<id>\d+)/?$', token_required(NoteView.as_view())),
    url(r'^search/?$', token_required(SearchView.as_view())),
]
