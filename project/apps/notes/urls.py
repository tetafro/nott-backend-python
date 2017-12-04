from django.conf.urls import url
from core.decorators import login_required_ajax
from .views import index, FolderView, NotepadView, NoteView, SearchView


urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^ajax/folders/?$', login_required_ajax(FolderView.as_view())),
    url(r'^ajax/folders/(?P<id>\d+)/?$', login_required_ajax(FolderView.as_view())),
    url(r'^ajax/notepads/?$', login_required_ajax(NotepadView.as_view())),
    url(r'^ajax/notepads/(?P<id>\d+)/?$', login_required_ajax(NotepadView.as_view())),
    url(r'^ajax/notes/?$', login_required_ajax(NoteView.as_view())),
    url(r'^ajax/notes/(?P<id>\d+)/?$', login_required_ajax(NoteView.as_view())),
    url(r'^ajax/search/?$', login_required_ajax(SearchView.as_view())),
]
