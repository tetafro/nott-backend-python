from django.conf.urls import url
from core.decorators import login_required_ajax
from .views_ajax import FolderView, NotepadView, NoteView, SearchView


urlpatterns = [
    url(r'^folders/?$', login_required_ajax(FolderView.as_view())),
    url(r'^folders/(?P<id>\d+)/?$', login_required_ajax(FolderView.as_view())),
    url(r'^notepads/?$', login_required_ajax(NotepadView.as_view())),
    url(r'^notepads/(?P<id>\d+)/?$', login_required_ajax(NotepadView.as_view())),
    url(r'^notes/?$', login_required_ajax(NoteView.as_view())),
    url(r'^notes/(?P<id>\d+)/?$', login_required_ajax(NoteView.as_view())),
    url(r'^search/?$', login_required_ajax(SearchView.as_view())),
]
